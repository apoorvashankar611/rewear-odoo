# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q 

from .models import ClothingItem, SwapRequest
from .forms import ClothingItemForm, CustomUserCreationForm

def home_view(request):
    items = ClothingItem.objects.filter(is_approved=True, status='available')
    context = {'items': items}
    return render(request, 'core/home.html', context)

def item_detail_view(request, pk):
    item = get_object_or_404(ClothingItem, pk=pk, is_approved=True)
    context = {'item': item}
    return render(request, 'core/item_detail.html', context)

# --- Authentication Views ---

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log the user in automatically after signing up
            return redirect('core:home')
    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'core/signup.html', context)

# --- Item Management Views ---

@login_required
def add_item_view(request):
    if request.method == 'POST':
        form = ClothingItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            return redirect('core:dashboard')
    else:
        form = ClothingItemForm()
    context = {'form': form}
    return render(request, 'core/add_item.html', context)

# --- Dashboard and Swapping Views ---

@login_required
def dashboard_view(request):
    my_items = ClothingItem.objects.filter(owner=request.user)
    # Requests other people made for MY items
    incoming_requests = SwapRequest.objects.filter(item_requested__owner=request.user, status='pending')
    # Requests I made for OTHER people's items
    outgoing_requests = SwapRequest.objects.filter(requester=request.user)
    
    context = {
        'my_items': my_items,
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def request_swap_view(request, item_pk):
    item_to_request = get_object_or_404(ClothingItem, pk=item_pk)
    
    # Prevent users from requesting their own items
    if item_to_request.owner == request.user:
        # Maybe add a Django message here later
        return redirect('core:item_detail', pk=item_pk)
        
    # Create the swap request
    SwapRequest.objects.get_or_create(
        requester=request.user,
        item_requested=item_to_request,
        defaults={'status': 'pending'} # Only create if it doesn't exist
    )
    return redirect('core:dashboard')

@login_required
def accept_swap_view(request, swap_pk):
    swap = get_object_or_404(SwapRequest, pk=swap_pk, item_requested__owner=request.user)
    
    if swap.status == 'pending':
        item = swap.item_requested
        
        # Update item status
        item.status = 'swapped'
        item.save()
        
        # Transfer points
        owner = item.owner
        owner.points += item.points_value
        owner.save()
        
        # Mark swap as accepted
        swap.status = 'accepted'
        swap.save()
        
        # Reject all other pending requests for this item
        SwapRequest.objects.filter(item_requested=item, status='pending').update(status='rejected')

    return redirect('core:dashboard')

@login_required
def decline_swap_view(request, swap_pk):
    swap = get_object_or_404(SwapRequest, pk=swap_pk, item_requested__owner=request.user)
    if swap.status == 'pending':
        swap.status = 'rejected'
        swap.save()
    return redirect('core:dashboard')


# core/views.py
# (Add these two new functions to the file. You can put them at the end.)

@login_required
def checkout_view(request, item_pk):
    item = get_object_or_404(ClothingItem, pk=item_pk)
    context = {
        'item': item
    }
    # In a real app, this view would handle a form submission with payment details.
    # For our mock-up, just showing the page is enough.
    return render(request, 'core/checkout.html', context)

@login_required
def purchase_success_view(request):
    # This is a static success page. In a real app, you'd pass the item_pk
    # and update its status to 'sold' here after successful payment.
    # For the demo, we'll just show a success message.
    return render(request, 'core/purchase_success.html')
