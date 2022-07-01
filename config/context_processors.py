from django.utils.safestring import mark_safe


def get_breadcrumb(request):
    """
        Generate Breadcrumb(secondary navigation scheme).
    """
    url_path = [url for url in request.path.split("/") if url]
        
    arrow_icon = """<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1" width="15px">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" /></svg>"""
    
    logo = """<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1" width="24px">
        <path stroke-linecap="round" stroke-linejoin="round" d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" /></svg>"""
            
    breadcrumb_html = logo + f"<a href='/'>Home</a>" + arrow_icon
    
    
    for counter, sub_path in enumerate(url_path):
        href = "/".join(url_path[:counter+1])
        if url_path[counter] == url_path[-1]:
            breadcrumb_html += f"""<li class="active"><em>{sub_path}</em></li>"""
        else:
            breadcrumb_html += f"""<a href='/{href}'>{sub_path}</a>""" + arrow_icon
            
    return {"get_breadcrumb": mark_safe(breadcrumb_html)}
