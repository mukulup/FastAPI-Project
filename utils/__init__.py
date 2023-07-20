import math


def objectsList(schema, entity):
    return [schema(item) for item in entity]

def paginate_data(total_records, data, page_no, page_size):
    previous_page = current_page = next_page = None
    total_pages = 0
    if data:
        total_pages = math.ceil(total_records/page_size)
        current_page = page_no
        previous_page = None if current_page == 1 else current_page - 1
        next_page = None if current_page == total_pages else current_page + 1

    paginated_response = {
        "total_records": total_records,
        "previous_page": previous_page,
        "current_page": current_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "data": data,
    }

    return paginated_response