# from django.views.generic import View

from .models import PageNotFound

# # Create your views here.
# class Handler404(View):
#     template_name = '404.html'
#     # model = PageNotFound

#     def get_context_data(self, **kwargs):
#         context = super(Handler404, self).get_context_data(**kwargs)
#         context['page_404'] = PageNotFound.objects.filter(active=True).order_by('?')[0]
#         return context

# handler_404 = Handler404.as_view()

from django.shortcuts import render
 
def handler_404(request):
    context = PageNotFound.objects.filter(active=True).order_by('?')[0]
    return render(request, '404.html', {'error_404': context})
