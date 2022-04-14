from django.shortcuts import render
from django.views.generic import TemplateView
from products.models import Product


# Create your views here.

class CartMain(TemplateView):
    template_name = 'cart/cart_main.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # Get the value (<button name="">) from pressed button.
        # This condition deletes all items from the cart.
        if request.POST.get('item_to_remove') == 'all':
            # 'request.session.modified = True' is mandatory when you
            # CHANGE or ADD the contents of the items in the 'request.session'
            # but not DELETE the 'request.session' itself
            try:
                del request.session['cart_items']
                request.session.modified = True

                del context['cart_items']
                # KeyError can be caught when user has already deleted items
                # from the cart, pressed 'back' in URL bar and tried to delete
                # items (one or all) again
            except KeyError:
                pass
        # This condition is just in case someone POST's to this page not by 
        # clicking any of the buttons on the page, but by some accident.
        elif request.POST.get('item_to_remove') is None:
            return render(
                request,
                self.template_name,
                context
            )
        # This condition deletes only specified product in the list.
        else:
            index_of_removed_item = int(request.POST.get('item_to_remove'))
            try:
                del request.session['cart_items'][index_of_removed_item]
                request.session.modified = True

                del context['cart_items'][index_of_removed_item]
            except KeyError:
                pass
        return render(
            request,
            self.template_name,
            context
        )

    # First we get object ID from the 'request.session['cart_items']', like
    # from '/products/2' we get int(2), then we get the 'object_instance'
    # using 'Product.objects.get(id=object_id)', then we make a list of all
    # the objects.
    def get_objects_from_url(self, *args, **kwargs):
        # If there are no items in 'request.session', meaning no items in
        # 'self.request.session['cart_items']', which leads to raising 
        # "KeyError: 'cart_items'". So, we catch this exception and return
        # the abscence of objects, meaning we return 'None'
        try:
            objects_url_list = self.request.session['cart_items']
            objects_list = []
            for object_url in objects_url_list:
                object_id = int(object_url[10:len(object_url)-1])
                object_instance = Product.objects.get(id=object_id)
                objects_list.append(object_instance)
            return objects_list
        except KeyError:
            return None
        
    # Thanks to the 'request.sessions' middleware and 'products_detail_view'
    # of the 'products' app we got the URLs of the products that were added to
    # the cart. Now all we have to do is get the objects themselves using the
    # same URL.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_items'] = self.get_objects_from_url()
        return context
