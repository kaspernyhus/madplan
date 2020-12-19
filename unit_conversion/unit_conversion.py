def convert_amount(from_unit, to_unit, amount):
    # "1"	"stk"
    # "2"	"kg"
    # "3"	"g"
    # "4"	"l"
    # "5"	"dl"
    # "6"	"cl"
    # "7"	"ml"
    # "8"	"tsk"
    # "9"	"spsk"
    # "10"	"dåse"
    # "11"	"bakke"
    # "12"	"pose"
    # "13"	"glas"
    # "14"	"bøtte"
    # "15"	"fed"
    # "16"	"håndfuld"
    # "17"	"knivspids"

    conversion_table = [
        [],
        #      stk   kg    g     l     dl    cl    ml    tsk   spsk  dåse  bakke pose  glas  bøtte fed håndfuld knivspids
        [None, 1   , None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],  # stk
        [None, None, 1   , 1000, None, None, None, None, None, None, None, None, None, None, None, None, None, None],  # kg
        [None, None, 0.001,1   , None, None, None, None, None, None, None, None, None, None, None, None, None, None],  # g
        [None, None, None, None, 1   , 10  , 100 , 1000, None, None, None, None, None, None, None, None, None, None],  # l
        [None, None, None, None, 0.1 , 1   , 10  , 100 , None, None, None, None, None, None, None, None, None, None],  # dl
        [None, None, None, None, 0.01, 0.1 , 1   , 10  , None, None, None, None, None, None, None, None, None, None],  # cl
        [None, None, None, None, 0.001,0.01, 0.1 , 1   , 1/5 , 1/15, None, None, None, None, None, None, None, None],  # ml
        [None, None, None, None, None, None, None, 5   , 1   , 1/3 , None, None, None, None, None, None, None, 22  ],  # tsk
        [None, None, None, None, None, None, None, 15  , 3   , 1   , None, None, None, None, None, None, None, None],  # spsk
        [None, None, None, None, None, None, None, None, None, None, 1   , None, None, 1   , None, None, None, None],  # dåse
        [None, None, None, None, None, None, None, None, None, None, None, 1   , None, None, None, None, None, None],  # bakke
        [None, None, None, None, None, None, None, None, None, None, None, None, 1   , None, None, None, None, None],  # pose
        [None, None, None, None, None, None, None, None, None, None, 1   , None, None, 1   , 1   , None, None, None],  # glas
        [None, None, None, None, None, None, None, None, None, None, None, None, None, 1   , 1   , None, None, None],  # bøtte
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1   , None, None],  # fed
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1   , None],  # håndfuld
        [None, None, None, None, None, None, None, None, 1/22, None, None, None, None, None, None, None, None, 1   ],  # knivspids
    ]
    if conversion_table[from_unit][to_unit]:
        return conversion_table[from_unit][to_unit]*amount
    else:
        return False