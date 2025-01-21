import pandas as pd
from django.shortcuts import render
from .forms import SearchForm
from django.core.paginator import Paginator

def load_csv():
    # Load CSV data
    df = pd.read_csv('search/data.csv')
    return df

def index(request):
    df = load_csv()
    search_query = request.GET.get('search', '')
    jl_date_filter = request.GET.get('jl_date', '')  # Change 'ol_date' to 'jl_date'

    # Filter by username if search query exists
    filtered_data = df[df['usrname'].str.contains(search_query, case=False)] if search_query else df
    
    # Exclude records where 'usrname' contains '@tcsrh.com' or '@tcshub'
    filtered_data = filtered_data[~filtered_data['usrloginid'].str.contains('@tcsrh.com|tcshub', case=False, na=False)]
    
    # Filter by JL_date if the dropdown selection exists
    if jl_date_filter:
        filtered_data = filtered_data[filtered_data['JL_date'] == jl_date_filter]  # Change 'OL_date' to 'JL_date'
    
    # Pagination
    paginator = Paginator(filtered_data.to_dict('records'), 100)  # 100 rows per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get unique JL_date for the dropdown
    jl_dates = df['JL_date'].dropna().unique()  # Change 'OL_date' to 'JL_date'

    # Add serial number (S.No) based on the page number
    start_index = page_obj.start_index()
    for idx, record in enumerate(page_obj.object_list):
        record['SNo'] = start_index + idx

    context = {
        'data': page_obj,
        'search_form': SearchForm(),
        'jl_dates': jl_dates,  # Change 'ol_dates' to 'jl_dates'
    }
    return render(request, 'search/index.html', context)
