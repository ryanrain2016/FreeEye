from django import forms, template


register = template.Library()

@register.filter
def cvtmem(mem):
    if mem=='':return ''
    mem = int(mem)
    units = ['KB','MB','GB']
    unit_index = 0
    while mem>1024:
        unit_index += 1
        mem/=1024
    return '%.2f%s'%(mem,units[unit_index])

