from newspapers import newspaper_CBC, newspaper_LaNueva, newspaper_Clarin, newspaper_Pagina12

mapping_newspaper = {
    "clarin": newspaper_Clarin,
    "lanueva": newspaper_LaNueva,
    "cbc": newspaper_CBC,
    "pagina12": newspaper_Pagina12
}


def get_valid_newspaper_str():
    valid_newspaper = list(mapping_newspaper)
    str_ret = ", ".join(valid_newspaper[:-1])
    return str_ret + " or " + valid_newspaper[-1]
