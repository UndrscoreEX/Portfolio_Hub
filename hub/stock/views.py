from django.shortcuts import render
from .Stock_eval import full_stock_evaluation


def index(request):
    return render(request, "core/index.html")

def stock_info(request):
    api_key = request.POST.get('api_key')  
    stock_code = request.POST.get('code')  
    print("pre data check", api_key, stock_code) 
    if not api_key or not stock_code:
        return render(request, "core/_stock_result.html", {
            "error": "⚠️ missing Key or Ticker is missing. Please retry. ⚠️"
        })    

    data = full_stock_evaluation(stock_code, api_key)
    print("post data check")

    if not data:
        return render(request, "core/_stock_result.html", {
            "error": "⚠️ API key or Ticker is invalid. Please retry. ⚠️"
        })

    return render(request, "core/_stock_result.html", {"data": data})

def example_result_view(request):
    return render(request, 'core/_example_result.html')

