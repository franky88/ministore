import django_tables2 as tables

from .models import Product

def rows_higlighter(**kwargs):  
    # Add highlight class to rows 
    # when the product is recently updated.
    # Recently updated rows are in the table
    # selection parameter.  
    selected_rows = kwargs["table"].selected_rows  
    if selected_rows and kwargs["record"].pk in selected_rows:  
        return "highlight-me"  
    return ""