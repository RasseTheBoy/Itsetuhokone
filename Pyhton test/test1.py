from FastDebugger import fd


def pprint(*texts, do_print:bool=True, debug_print:bool=True):
    """Print info.
    Mainly used for debugging.
    
    Parameters:
    - `texts`: Texts to print; can be multiple
    - `do_print`: If `True`, print; if `False`, do not print"""
    
    if not (do_print and debug_print):
        return

    # Print first item
    if len(texts) == 1:
        print(f'{name}: {texts[0]}')
        return
    
    print(f'{name}: {texts[0]}', end=' ')

    # Print other items without name; except last item
    for item in texts[1:-1]:
        print(item, end=' ')

    print(texts[-1]) # Print last item

        

        



name = 'Rasmus'
l = 'hello world again. Why are we here?'.split(' ')

# fd(l[1:-1])

pprint(*l, debug_print=True)
pprint('who are you?')
pprint('now')