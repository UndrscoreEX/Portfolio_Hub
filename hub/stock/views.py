from django.shortcuts import render
from .Stock_eval import full_stock_evaluation


def index(request):
    return render(request, "core/index.html")

def stock_info(request):
    api_key = request.POST.get('api_key')  
    stock_code = request.POST.get('code')  
    # maybe add a popup if the API key doesnt work. 
    if not stock_code:
        return render(request, "core/_stock_result.html", {
            "error": "⚠️ Ticker is missing (or my API key has run out so add a new one). Please retry. ⚠️"
        })    
    if api_key :
        data = full_stock_evaluation(stock_code, api_key)
    else:
        data = full_stock_evaluation(stock_code)
    # data = full_stock_evaluation(stock_code, API_KEY)
    print("post data check")
    
    if not data:
        return render(request, "core/_stock_result.html", {
            "error": "⚠️ Ticker is missing (or my API key has run out so add a new one). Please retry. ⚠️"
        })

    return render(request, "core/_stock_result.html", {"data": data})

def example_result_view(request):
    return render(request, 'core/_example_result.html')

