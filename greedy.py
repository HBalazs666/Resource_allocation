


def ms_order_by_RAM(ms_list):

    # csökkenő sorrend
    ms_list.sort(key=lambda x: x.RAM_req, reverse=True)

    return