from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import Group
from .forms import ProductForm, SearchForm
from .models import Product, Category, Maker


def products_all_view(request):
    # Getting the workers' username to check in template if we should add
    # 'add product' button.
    g = Group.objects.get(name='Workers')
    workers_username = [
        group_user.get('username') for group_user in g.user_set.values()
    ]

    all_products = Product.objects.order_by('id')
    all_categories = Category.objects.all()
    all_makers = Maker.objects.all()
    
    # Condition to know how many products per page a person requested.
    if request.method == 'POST':
        try:
            products_per_page = request.POST.get('number_of_objects_on_page')
            paginator = Paginator(all_products, products_per_page, allow_empty_first_page=True)
            request.session['products_per_page'] = products_per_page
            request.session.modified = True
        except ValueError:
            paginator = Paginator(all_products, 2, allow_empty_first_page=True)
    
    # If user didn't change the num. of objects to display on page, display 2.
    # else display the number requested and saved in 'request.session'
    try:
        paginator = Paginator(
            all_products,
            request.session['products_per_page'],
            allow_empty_first_page=True
        )
    except KeyError:
        paginator = Paginator(all_products, 2, allow_empty_first_page=True)

    # page that is requested by the user
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    context = {
        'workers_username': workers_username,
        'all_products': all_products,
        'all_categories': all_categories,
        'all_makers': all_makers,
        'page_object': page_object
    }
    return render(request, 'products/all.html', context)


# The view used to add new products to the database.
# It allows authenticated users in 'Workers' group and superuser
# to add products. Doesn't allow unathenticated users and non-'Workers'
def products_add_view(request):
    # This is a standard Django syntax to get group name from database.
    g = Group.objects.get(name='Workers')
    # getting the user from the request 
    # (this is done via Django sessions middleware)
    u = request.user
    
    # 'g' is a group object which has 'user_set' "attribute" (not actually)
    # which contains all the users of the group 'g', who we then get using
    # '.values()' method, which returns a dictionary full of related and not
    # key-value pairs. Then we get all the usernames of workers
    workers_username = [key.get('username') for key in g.user_set.values()]
    if u.username in workers_username or u.is_superuser:
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance & populate it with data from the request:
            form = ProductForm(request.POST)
            # '.is_valid()' uses Django validation middleware to check 
            # validity and completeness of the data in the form.
            # If the data is not full in the form - raises an error.
            if form.is_valid():
                form.save()
                return redirect('products-all')
        else:
            form = ProductForm()

        context = {
            'form': form,
        }
        return render(request, 'products/add.html', context)
    else:
        raise Http404("You aren't authorised to add stuff!")

def products_detail_view(request, id_):
    product = get_object_or_404(Product, id=id_)

    # We get the workers_username to check (inside of html) if the user in the
    # authorised group or not. If yes, he gets 2 extra buttons there.
    g = Group.objects.get(name='Workers')
    workers_username = [
        group_user.get('username') for group_user in g.user_set.values()
    ]
    context = {
        'workers_username': workers_username,
        'product': product,
        'title': product.title,
        'description': product.description,
        'category': product.category,
        'maker': product.maker,
        'price': product.price,
        'country_of_origin': product.get_country_of_origin_display,
    }

    # If request is POST, it means that the 'Add to cart' button was clicked,
    # which means we have to add the product to the cart. We do it via
    # 'sessions' middleware. We add the 'product.get_absolute_url()' to the
    # session's 'cart_items' variable, then, in the 'CartMain' view of 'Cart'
    # app, using the URL get the corresponding ID of a product.
    if request.method == 'POST':
        if request.user.is_authenticated:
            # !!!!! COPY FROM 'cart.views.CartMain' VIEW !!!!!
            # If there are no items in 'request.session', meaning no items in
            # 'self.request.session['cart_items']', which leads to raising 
            # "KeyError: 'cart_items'". So, we catch this exception and return
            # the abscence of objects, meaning we return 'None'
            try:
                cart_items = request.session['cart_items']
            except KeyError:
                cart_items = []
            cart_items.append(product.get_absolute_url())

            request.session['cart_items'] = cart_items
            request.session.modified = True

            return render(request, 'products/detail.html', context)
        else:
            context['wrong_credentials'] = True
            return render(request, 'products/detail.html', context)
    else:
        return render(request, 'products/detail.html', context)


def products_update_view(request, id_):
    product_to_update = get_object_or_404(Product, id=id_)
    
    g = Group.objects.get(name='Workers')
    u = request.user
    workers_username = [
        group_user.get('username') for group_user in g.user_set.values()
    ]

    if u.username in workers_username or u.is_superuser:
        if request.method == 'POST':
            # add a needed 'instance' kwarg to update the chosen product
            form = ProductForm(request.POST, instance=product_to_update)
            if form.is_valid():
                form = ProductForm(request.POST, instance=product_to_update)
                form.save()
                return redirect('products-all')
        else:
            form = ProductForm(instance=product_to_update)
        context = {
            'form': form,
            'product': product_to_update,
        }
        return render(request, 'products/update.html', context)
    else:
        raise Http404("You aren't authorised to update stuff!")


def products_filter_view(request):
    form = SearchForm(request.GET)

    # On the first visit to the web-page the request.GET is empty.
    # After we filter the results using the form,
    # we get information in our request.GET (URL), i.e. 
    # '../filter/?maker=3&category=8&country_of_origin=RU&type=foo'.
    # If there's no data after any keyword (maker=&category=8, for example)
    # (notice the lack of number after 'maker='),
    # we get an error, saying that in order to filter the queryset
    # Django needs some ID. And I couldn't find any way to manipulate ID,
    # so I decided to manipulate the GET request itself.

    # This function is used to get all the indexes of different attributes
    # of product (all categories' ID's, all makers' ID's).
    # The good thing about such method is the fact that it's scalable,
    # meaning you can add as much one-to-many fields as you want in the model
    # and form.
    def get_all_indexes_of_empty_items(empty_item):
        item_queryset = form.fields.get(empty_item).queryset
        item_list = [item_objects for item_objects in item_queryset]
        all_item_id = [
            item_list[index].id for index, item in enumerate(item_list)
        ]
        return all_item_id

    # Because the request object is immutable, 
    # we create a copy of the request, which is mutable. 
    # After that we pop every empty value from the
    # new_request, transforming the request.GET 'body' from
    # 'maker=3&category=' to 'maker=3', which is then
    # passed to filter. The URL remains the same as if nothing's changed
    # compared to original request
    new_request = request.GET.copy()
    for i in request.GET.items():
        if i[1] == '':
            new_request.pop(i[0])
    # We make a mutable copy of QueryDict (request.GET) without empty values
    # QueryDict makes automatic lists when new values are added to it
    # meaning if we add a list of values, they get coated into another list
    # (list of lists) which really messes up the process.
    # So we turn the QueryDict into a normal dict using the .dict() method
    new_request = new_request.dict()

    # Magnum Opus or the logic of everything done beforehand:
    # if we choose all filters, then everything's good and this conditional
    # cycle just skips;
    # if we don't choose all filters (1/2, for example) the problem arises
    # with the fact that an empty string ('') is passed to the filter.
    # This here is a workaround about this. We get the IDs of the 
    # product attributes i. e. all categories' IDs 
    # ([1, 2, 3, 4, ...]), 
    # all makers' IDs 
    # ([1, 2, 3, 4, ...] or if they were strings: [Sony, ASUS, HP, ...])
    # and put them into a 'new_request' dictionary, from where the next code
    # after this gets (literally 'new_request.get') the values
    for i in request.GET.items():
        if i[1] == '':
            all_indexes = get_all_indexes_of_empty_items(i[0])
            new_request.update({i[0]: all_indexes})

    # if the request.GET is empty (meaning we've visited the page first time)
    # we display the filtered products
    # else we don't display anything
    if bool(request.GET) == True:
        displayed_products = Product.objects.all().filter(
                # __in is a lifesaver
                maker_id__in=new_request.get('maker'),
                category_id__in=new_request.get('category'),
                # Because in the beginning I decided for some reason that it
                # would be a cool idea to have all the countries hard-coded
                # into a separate file instead of holding them in a database
                # via a separate model, the mechanism to filter products by
                # countries differs from the one implemented for other fields.
                # I don't want to make this view bigger than it already is
                # (especially considering the comments), so I've decided to
                # drop the feature of filtering by the country of origin.
                # If needs be, then I will add it later.
            )
    else:
        # If no filters were chosen on the second visit to the web-page,
        # then all products are shown, instead of none. 
        # This is indeed not a bug, but a feature.
        displayed_products = None

    context = {
        'form': form,
        'displayed_products': displayed_products,
        'url': request.path,
    }
    return render(request, 'products/filter.html', context)


def products_delete_view(request, id_):
    g = Group.objects.get(name='Workers')
    u = request.user
    workers_username = [
        group_user.get('username') for group_user in g.user_set.values()
    ]
    
    product_to_delete = get_object_or_404(Product, id=id_)
    if u.username in workers_username or u.is_superuser:
        if request.method == 'POST':
            product_to_delete.delete()
            return redirect('products-all')
        else:
            context = {
                'product_to_delete': product_to_delete,
                'product_title': product_to_delete.title,
                'product_description': product_to_delete.description,
            }
            return render(request, 'products/delete.html', context)
    else:
        raise Http404("You aren't authorised to delete stuff!")


def products_maker_view(request, id_):
    maker = get_object_or_404(Maker, id=id_)
    context = {
        'maker': maker
    }
    return render(request, 'products/maker.html', context)
