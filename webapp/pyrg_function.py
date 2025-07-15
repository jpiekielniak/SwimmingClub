def convert2range(v, f_min, f_max, t_min, t_max):
    """Funkcja konwertuje przekazaną wartość (v) z zakresu od f_min
    do f_max, na odpowiadającą jej wartość z zakresu t_min do t_max.

    Kod bazuje na technic opisanej na stronie:
        http://james-ramsden.com/map-a-value-from-one-number-scale-to-another-formula-and-c-code/
    """
    return round(t_min + (t_max - t_min) * ((v - f_min) / (f_max - f_min)), 2)
