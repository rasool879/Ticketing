from random import randint

def get_ref_nom(model, digits=10):
    ref_no = randint(10**(digits-1), 10**digits-1)
    while model.objects.filter(ref_no=ref_no):
        ref_no = randint(10**(digits-1), 10**digits-1)
    return ref_no

