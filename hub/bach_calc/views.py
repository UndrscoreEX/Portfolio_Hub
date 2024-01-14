from django.shortcuts import render
from django.views import View
from .models import Height_groups, Income_groups, Age_ref
from django.db.models import Sum

# notes of my plan:
# 5-year groups from 20-80 (this means we will have a lower pop than JP total)
# 

def Calc_form_specs(form_data):

    results = {
                'min_age': form_data.POST['mn_age_value'],
                'max_age':str(int(form_data.POST['mx_age_value']) -1),
                'income' :form_data.POST['income_value'],
                'n_obese':form_data.POST.get('n_obese_value', False),
                'height':form_data.POST.get('height_value'),
                'n_married': form_data.POST.get('n_married_value',False),
                'n_smoker': form_data.POST.get('n_smoke',False),
            }
    pop_range = Age_ref.objects.filter(age__gte=results['min_age'],age__lte=results['max_age'])
    
    # values that will be added to for each age group
    total_pop = 0
    not_married_num = 0
    income_num = 0
    n_obese_total = 0
    n_smoke_num = 0

    # age groups are the base. From here we find each percent of each condition for each group.
    for x in pop_range:
        this_age_group_pop = x.age_group_pop
        this_age_g_inc_perc = 0

        if results['n_obese']:
            n_obese_total += ((x.not_obese_rate/100) * x.age_group_pop)
        if results['n_married']:
            not_married_num += x.n_yet_married
        if results['n_smoker']:
            n_smoke_num += ((x.not_smoke_rate/100) *x.age_group_pop)

        # now, for each age group, search table for that age group's income brackets
        inc_yr_groups = x.income_groups.filter(income_yr__gte=results['income'])
        for inc in inc_yr_groups:
            this_age_g_inc_perc = round((this_age_g_inc_perc + inc.income_ratio),1) 
        income_num += this_age_g_inc_perc*this_age_group_pop

        # total popularions of chosen age group.
        total_pop += this_age_group_pop

    # Find percent of each value vs the total pop (rate of X)
    n_marr_final_per = not_married_num/total_pop
    obese_final_per = n_obese_total/total_pop
    n_smoke_final_per = n_smoke_num/total_pop
    abv_inc_range_per = income_num/total_pop

    final_amount_of_people = total_pop

    # applying rates for each condition to the final number:
    if n_marr_final_per: 
        final_amount_of_people *= n_marr_final_per
    if obese_final_per:
        final_amount_of_people *= obese_final_per
    if n_smoke_final_per:
        final_amount_of_people *= n_smoke_final_per
    if abv_inc_range_per:
        final_amount_of_people *= abv_inc_range_per

    # If there was an adjustment to the height bar:
    if results['height'] != '139':
        height_per = Height_groups.objects.filter(height_cm__gte= results['height']).aggregate(Sum('ht_per'))
        final_amount_of_people *= (height_per['ht_per__sum'] /100)

    ultimate_num = final_amount_of_people/total_pop
    results['final'] = round(ultimate_num,2)
   
    return results




class Calculate_spec(View):

    def get(self, request):
        
        return render(request, 'bach_calc/index.html')

    def post(self, request):
        
        clean_results = Calc_form_specs(request)
        return render(request, 'bach_calc/results.html', {'results':clean_results} )

class Stats_en(View):
    def get(self, request):
        return render(request, 'bach_calc/stats_en.html')



class Calculate_spec_jp(View):

    def get(self, request):
        
        return render(request, 'index_jp.html')

    def post(self, request):

        clean_results = Calc_form_specs(request)
        return render(request, 'bach_calc/results_jp.html', {'results':clean_results} )

class Stats_jp(View):
    def get(self, request):
        return render(request, 'bach_calc/stats_jp.html')
