from django.http import Http404
from django.urls import reverse
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView
)

from rest_framework import viewsets

from penny.mixins import AgentRequiredMixin
from ui.views.base_views import BaseContextMixin, PublicReactView
from listings.forms import ListingForm, ListingDetailForm, ListingPhotosForm
from listings.models import Listing, ListingDetail, ListingPhotos
from listings.serializer import (
    PublicListingSerializer, PrivateListingSerializer
)
from listings.constants import (
    PETS_ALLOWED, AMENITIES, LISTING_TYPES, LISTING_STATUS
)
from listings.utils import filter_listings


class WizardMixin:
    pk_url_kwarg = 'pk'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listing = None
        self.listing_qs = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listing'] = self.get_listing()
        return context

    def get_object(self, queryset=None):
        self.listing = self.get_listing()
        queryset = self.get_queryset()
        obj, _ = queryset.get_or_create(listing=self.listing)
        return obj

    def get_listing_qs(self):
        self.listing_qs = Listing.objects.all()
        return self.listing_qs

    def get_listing(self):
        if self.listing:
            return self.listing

        queryset = self.get_listing_qs()
        try:
            pk = self.kwargs.get(self.pk_url_kwarg)
            # Get the single item from the filtered queryset
            obj = queryset.get(pk=pk)
        except queryset.model.DoesNotExist:
            raise Http404(f"No {queryset.model._meta.verbose_name}s "
                          f"found matching the query")
        return obj


class MainListingCreate(AgentRequiredMixin, CreateView):
    template_name = 'listings/main_listing.html'
    model = Listing
    form_class = ListingForm

    def get_success_url(self):
        return reverse("listings:detail", kwargs={'pk': self.object.id})


class MainListingUpdate(AgentRequiredMixin, UpdateView):
    template_name = 'listings/main_listing.html'
    model = Listing
    form_class = ListingForm

    def get_success_url(self):
        return reverse("listings:detail", kwargs={'pk': self.object.id})


class DetailListingUpdate(AgentRequiredMixin, WizardMixin, UpdateView):
    template_name = 'listings/detail_listing.html'
    model = ListingDetail
    form_class = ListingDetailForm

    def get_success_url(self):
        return reverse("listings:photos", kwargs={'pk': self.listing.id})


class PhotosListingUpdate(AgentRequiredMixin, WizardMixin, UpdateView):
    template_name = 'listings/photos_listing.html'
    model = ListingPhotos
    form_class = ListingPhotosForm

    def get_success_url(self):
        return reverse("listings:review", kwargs={'pk': self.listing.id})


class ReviewListing(BaseContextMixin, WizardMixin, TemplateView):
    template_name = 'listings/review_listing.html'

    def get_listing_qs(self):
        self.listing_qs = super().get_listing_qs()
        self.listing_qs = self.listing_qs.select_related(
            'detail', 'photos', 'listing_agent', 'sales_agent'
        )
        return self.listing_qs


class Listings(AgentRequiredMixin, PublicReactView):
    title = 'Listings Management'
    component = 'pages/listings.js'

    def props(self, request, *args, **kwargs):
        constants = {
            'pets_allowed': dict(PETS_ALLOWED),
            'amenities': {
                amenity_tuple[0]: amenity_tuple[1]
                for _, group in dict(AMENITIES).items()
                for amenity_tuple in group
            },
            'listing_types': dict(LISTING_TYPES),
            'listing_status': dict(LISTING_STATUS),
        }

        return {
            'constants': constants,
            'endpoint': '/listings/private/'
        }


class ListingDetail(BaseContextMixin, DetailView):
    model = Listing
    template_name = 'listings/listing_detail.html'

    def get_queryset(self):
        return Listing.objects.select_related(
            'detail', 'photos', 'listing_agent',
        )


# ViewSets define the view behavior.
class PublicListingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = PublicListingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            status='approved',
            detail__private=False
        )

        queryset = filter_listings(queryset, self.request.query_params)

        # remember to use always the page param
        # http://localhost:8000/listings/public/?page=1&price_min=3000
        return queryset.order_by('-created')


# ViewSets define the view behavior.
class PrivateListingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = PrivateListingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = filter_listings(queryset, self.request.query_params)
        return queryset.order_by('-created')
