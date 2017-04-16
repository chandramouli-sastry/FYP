import json
import os

from FactGen.NumericRatioFact import NumericRatioFact
from FactGen.SimpleStatisticFact import SimpleStatisticFact
from Resources import discrete_fields, new_fields
from FactGen.SemanticStatistic_binary import SemanticStatisticFact
print("Loading Partitions...")
partitions = json.load(open("Resources/partitions.json"))
DEBUG = False

def gen_simple():
    fields = discrete_fields + new_fields
    count = 0
    thresh = 1
    for field in fields:
        path = "JSONS/Simple/Fact_{}.json".format(field)
        print(field)
        if not (os.path.isfile(path)):
            print("==========================================================================================")
            s = SimpleStatisticFact(field=field,fileName=path,debug=DEBUG)
            s.partitions = partitions
            s.fuzzy_intersection()
            print("==========================================================================================")
        count += 1
        perc = count/len(fields)*100
        if perc>thresh:
            print("{}% completed".format(perc))
            thresh += 1

def gen_semantic():
    fields = new_fields
    count = 0
    thresh = 1
    for field in fields:
        path = "JSONS/Semantic/Fact_{}.json".format(field)
        print(field)
        if not(os.path.isfile(path)):
            print("==========================================================================================")
            s = SemanticStatisticFact(field=field, fileName=path, debug=DEBUG)
            s.partitions = partitions
            s.fuzzy_intersection()
            print("==========================================================================================")
        count += 1
        perc = count / len(fields) * 100
        if perc > thresh:
            print("{}% completed".format(perc))
            thresh += 1

def gen_ratio():
    field_pairs = [(0.99893583832170829, 'Tot_Sched_Cas_Mal_Pop_of_Vil', 'Tot_Sched_Cas_Pop_of_Vil'), (0.99889050636635857, 'Tot_Sched_Trib_Mal_Pop_of_Vil', 'Tot_Sched_Trib_Pop_of_Vil'), (0.99886660331428601, 'Tot_Sched_Trib_Fem_Pop_of_Vil', 'Tot_Sched_Trib_Pop_of_Vil'), (0.99879888599778943, 'Tot_Sched_Cas_Fem_Pop_of_Vil', 'Tot_Sched_Cas_Pop_of_Vil'), (0.99846265072044038, 'Tot_Mal_Pop_of_Vil', 'Tot_Pop_of_Vil'), (0.99832876683274474, 'Tot_Fem_Pop_of_Vil', 'Tot_Pop_of_Vil'), (0.99551686179962773, 'Tot_Sched_Trib_Fem_Pop_of_Vil', 'Tot_Sched_Trib_Mal_Pop_of_Vil'), (0.99547615101149101, 'Tot_Sched_Cas_Fem_Pop_of_Vil', 'Tot_Sched_Cas_Mal_Pop_of_Vil'), (0.99366684209180178, 'Tot_Fem_Pop_of_Vil', 'Tot_Mal_Pop_of_Vil'), (0.99060232972882556, 'Mob_Heal_Clin_Par_Med_Staf_In_Pos_Num', 'Mob_Heal_Clin_Par_Med_Staf_Tot_Stren_Num'), (0.98560575171818599, 'Pow_Sup_For_Com_Us_Sum_April_Sep_per_day_in_Hour', 'Pow_Sup_For_Com_Us_Win_Oc_Mar_per_day_in_Hour'), (0.9841933518473136, 'Dis_Par_Med_Staf_In_Pos_Num', 'Dis_Par_Med_Staf_Tot_Stren_Num'), (0.97986188118584983, 'Pow_Sup_For_Agric_Us_Sum_April_Sep_per_day_in_Hour', 'Pow_Sup_For_Agric_Us_Win_Oc_Mar_per_day_in_Hour'), (0.97970404539656819, 'Tot_Fem_Pop_of_Vil', 'Tot_Hous'), (0.97875563134739829, 'Pow_Sup_For_Dom_Us_Sum_April_Sep_per_day_in_Hour', 'Pow_Sup_For_Dom_Us_Win_Oc_Mar_per_day_in_Hour'), (0.97748186363223977, 'Tot_Hous', 'Tot_Pop_of_Vil'), (0.97740840918781957, 'Pow_Sup_For_Al_User_Sum_April_Sep_per_day_in_Hour', 'Pow_Sup_For_Al_User_Win_Oc_Mar_per_day_in_Hour'), (0.97237291388495173, 'Tot_Hous', 'Tot_Mal_Pop_of_Vil'), (0.97084427642896343, 'Hos_Allop_Par_Med_Staf_In_Pos_Num', 'Hos_Allop_Par_Med_Staf_Tot_Stren_Num'), (0.96991342661294977, 'TB_Clin_Par_Med_Par_Med_Staf_In_Pos_Num', 'TB_Clin_Par_Med_Par_Med_Staf_Tot_Stren_Num'), (0.96843696492044007, 'Fam_Wel_Cen_Par_Med_Staf_In_Pos_Num', 'Fam_Wel_Cen_Par_Med_Staf_Tot_Stren_Num'), (0.96811005941947048, 'Hos_Allop_Doc_In_Pos_Num', 'Hos_Allop_Doc_Tot_Stren_Num'), (0.96755793712002391, 'Prim_Heal_Cen_Par_Med_Staf_In_Pos_Num', 'Prim_Heal_Cen_Par_Med_Staf_Tot_Stren_Num'), (0.96096724673761336, 'TB_Clin_Doc_In_Pos_Num', 'TB_Clin_Doc_Tot_Stren_Num'), (0.95384741071363277, 'Mob_Heal_Clin_Doc_In_Pos_Num', 'Mob_Heal_Clin_Doc_Tot_Stren_Num'), (0.95253150170991829, 'Vet_Hos_Doc_In_Pos_Num', 'Vet_Hos_Doc_Tot_Stren_Num'), (0.95214616175395206, 'Mat_An_Chil_Wel_Cen_Par_Med_Staf_In_Pos_Num', 'Mat_An_Chil_Wel_Cen_Par_Med_Staf_Tot_Stren_Num'), (0.94930092148070766, 'Prim_Heal_Sub_Cen_Par_Med_Staf_In_Pos_Num', 'Prim_Heal_Sub_Cen_Par_Med_Staf_Tot_Stren_Num'), (0.91975842943493913, 'Dis_Doc_In_Pos_Num', 'Dis_Doc_Tot_Stren_Num'), (0.91680621403059415, 'Mat_An_Chil_Wel_Cen_Doc_In_Pos_Num', 'Mat_An_Chil_Wel_Cen_Doc_Tot_Stren_Num'), (0.91217684110684272, 'Prim_Heal_Cen_Doc_In_Pos_Num', 'Prim_Heal_Cen_Doc_Tot_Stren_Num'), (0.88778773603380889, 'Fam_Wel_Cen_Doc_In_Pos_Num', 'Fam_Wel_Cen_Doc_Tot_Stren_Num'), (0.88066625968161383, 'Vet_Hos_Doc_Tot_Stren_Num', 'Vet_Hos_Num'), (0.86693243441627577, 'TB_Clin_Doc_Tot_Stren_Num', 'TB_Clin_Num'), (0.86502375888597793, 'Prim_Heal_Sub_Cen_Doc_In_Pos_Num', 'Prim_Heal_Sub_Cen_Doc_Tot_Stren_Num'), (0.86374381981225212, 'Vet_Hos_Doc_In_Pos_Num', 'Vet_Hos_Num'), (0.83813678514531265, 'TB_Clin_Doc_In_Pos_Num', 'TB_Clin_Num'), (0.83742291047007344, 'Prim_Heal_Sub_Cen_Num', 'Prim_Heal_Sub_Cen_Par_Med_Staf_In_Pos_Num'), (0.82784159444008232, 'Prim_Heal_Sub_Cen_Num', 'Prim_Heal_Sub_Cen_Par_Med_Staf_Tot_Stren_Num'), (0.8199024448547424, 'Prim_Heal_Cen_Doc_Tot_Stren_Num', 'Prim_Heal_Cen_Num'), (0.81373512464395859, 'Vet_Hos_Doc_Tot_Stren_Num', 'Vet_Hos_Par_Med_Staf_Tot_Stren_Num'), (0.81149645871625231, 'Mob_Heal_Clin_Num', 'Mob_Heal_Clin_Par_Med_Staf_Tot_Stren_Num'), (0.80975946640992857, 'Vet_Hos_Num', 'Vet_Hos_Par_Med_Staf_Tot_Stren_Num'), (0.80794020274953093, 'Mob_Heal_Clin_Num', 'Mob_Heal_Clin_Par_Med_Staf_In_Pos_Num'), (0.8064591597197408, 'Vet_Hos_Doc_In_Pos_Num', 'Vet_Hos_Par_Med_Staf_Tot_Stren_Num'), (0.79921067964082337, 'Prim_Heal_Cen_Doc_In_Pos_Num', 'Prim_Heal_Cen_Num'), (0.79686627195299953, 'TB_Clin_Doc_Tot_Stren_Num', 'TB_Clin_Par_Med_Par_Med_Staf_Tot_Stren_Num'), (0.79523290709365846, 'TB_Clin_Doc_Tot_Stren_Num', 'TB_Clin_Par_Med_Par_Med_Staf_In_Pos_Num'), (0.7800730686534767, 'TB_Clin_Doc_In_Pos_Num', 'TB_Clin_Par_Med_Par_Med_Staf_In_Pos_Num'), (0.77185070539951939, 'Mat_An_Chil_Wel_Cen_Doc_Tot_Stren_Num', 'Mat_An_Chil_Wel_Cen_Num'), (0.77119768513126685, 'TB_Clin_Doc_In_Pos_Num', 'TB_Clin_Par_Med_Par_Med_Staf_Tot_Stren_Num'), (0.75254231900938817, 'Hos_Allop_Doc_Tot_Stren_Num', 'Hos_Allop_Par_Med_Staf_Tot_Stren_Num'), (0.74854894247918713, 'Mat_An_Chil_Wel_Cen_Num', 'Mat_An_Chil_Wel_Cen_Par_Med_Staf_Tot_Stren_Num'), (0.74223371243962366, 'Prim_Heal_Cen_Doc_In_Pos_Num', 'Prim_Heal_Cen_Par_Med_Staf_In_Pos_Num'), (0.7418442577011094, 'Prim_Heal_Cen_Doc_In_Pos_Num', 'Prim_Heal_Cen_Par_Med_Staf_Tot_Stren_Num'), (0.74134453196810357, 'Fam_Wel_Cen_Doc_Tot_Stren_Num', 'Fam_Wel_Cen_Par_Med_Staf_Tot_Stren_Num'), (0.7394389474411116, 'Hos_Allop_Doc_Tot_Stren_Num', 'Hos_Allop_Par_Med_Staf_In_Pos_Num'), (0.73872951607405168, 'Fam_Wel_Cen_Doc_In_Pos_Num', 'Fam_Wel_Cen_Par_Med_Staf_In_Pos_Num'), (0.73132123032864194, 'Mat_An_Chil_Wel_Cen_Doc_Tot_Stren_Num', 'Mat_An_Chil_Wel_Cen_Par_Med_Staf_Tot_Stren_Num'), (0.7296445501413148, 'Fam_Wel_Cen_Doc_In_Pos_Num', 'Fam_Wel_Cen_Par_Med_Staf_Tot_Stren_Num'), (0.72750350987177059, 'Prim_Heal_Cen_Doc_Tot_Stren_Num', 'Prim_Heal_Cen_Par_Med_Staf_Tot_Stren_Num'), (0.72258641984709027, 'Mat_An_Chil_Wel_Cen_Doc_In_Pos_Num', 'Mat_An_Chil_Wel_Cen_Par_Med_Staf_Tot_Stren_Num'), (0.71906122199515854, 'Hos_Allop_Doc_In_Pos_Num', 'Hos_Allop_Par_Med_Staf_In_Pos_Num'), (0.71781205522759539, 'Mat_An_Chil_Wel_Cen_Doc_In_Pos_Num', 'Mat_An_Chil_Wel_Cen_Num'), (0.71746104752111439, 'Mat_An_Chil_Wel_Cen_Doc_In_Pos_Num', 'Mat_An_Chil_Wel_Cen_Par_Med_Staf_In_Pos_Num'), (0.71589198574819168, 'Prim_Heal_Cen_Num', 'Prim_Heal_Cen_Par_Med_Staf_Tot_Stren_Num'), (0.71369915617899404, 'Hos_Allop_Doc_In_Pos_Num', 'Hos_Allop_Par_Med_Staf_Tot_Stren_Num'), (0.70970317903601066, 'Dis_Doc_Tot_Stren_Num', 'Dis_Num'), (0.70692815562832778, 'Tot_Mal_Pop_of_Vil', 'Tot_Sched_Cas_Fem_Pop_of_Vil'), (0.70636089335670105, 'TB_Clin_Num', 'TB_Clin_Par_Med_Par_Med_Staf_Tot_Stren_Num'), (0.70629216347166701, 'Tot_Mal_Pop_of_Vil', 'Tot_Sched_Cas_Pop_of_Vil'), (0.70621269680567267, 'Mat_An_Chil_Wel_Cen_Num', 'Mat_An_Chil_Wel_Cen_Par_Med_Staf_In_Pos_Num'), (0.70414335978655695, 'Tot_Mal_Pop_of_Vil', 'Tot_Sched_Cas_Mal_Pop_of_Vil'), (0.7040774327039907, 'Tot_Pop_of_Vil', 'Tot_Sched_Cas_Fem_Pop_of_Vil'), (0.70275443408151284, 'TB_Clin_Num', 'TB_Clin_Par_Med_Par_Med_Staf_In_Pos_Num'), (0.70190671327648457, 'Tot_Pop_of_Vil', 'Tot_Sched_Cas_Pop_of_Vil'), (0.69898733678417413, 'Tot_Fem_Pop_of_Vil', 'Tot_Sched_Cas_Fem_Pop_of_Vil'), (0.69832290080006998, 'Tot_Pop_of_Vil', 'Tot_Sched_Cas_Mal_Pop_of_Vil'), (0.69643646912544921, 'Tot_Hous', 'Tot_Sched_Cas_Fem_Pop_of_Vil'), (0.69522203072220212, 'Tot_Fem_Pop_of_Vil', 'Tot_Sched_Cas_Pop_of_Vil'), (0.69103881184307625, 'Tot_Hous', 'Tot_Sched_Cas_Pop_of_Vil'), (0.69015191030653245, 'Tot_Fem_Pop_of_Vil', 'Tot_Sched_Cas_Mal_Pop_of_Vil'), (0.68973319742179862, 'Prim_Heal_Cen_Doc_Tot_Stren_Num', 'Prim_Heal_Cen_Par_Med_Staf_In_Pos_Num'), (0.68476083758156991, 'Fam_Wel_Cen_Doc_Tot_Stren_Num', 'Fam_Wel_Cen_Par_Med_Staf_In_Pos_Num'), (0.68444134567675108, 'Tot_Hous', 'Tot_Sched_Cas_Mal_Pop_of_Vil'), (0.68410482554263075, 'Prim_Heal_Cen_Num', 'Prim_Heal_Cen_Par_Med_Staf_In_Pos_Num'), (0.68015981114205148, 'Priv_Mid_School_Num', 'Priv_Sec_School_Num'), (0.6755788250682625, 'Dis_Doc_In_Pos_Num', 'Dis_Num'), (0.67506392209195287, 'Priv_Mid_School_Num', 'Priv_Prim_School_Num'), (0.67292892066115262, 'Mat_An_Chil_Wel_Cen_Par_Med_Staf_In_Pos_Num', 'TB_Clin_Par_Med_Par_Med_Staf_In_Pos_Num'), (0.67176745020144091, 'Mat_An_Chil_Wel_Cen_Doc_Tot_Stren_Num', 'Mat_An_Chil_Wel_Cen_Par_Med_Staf_In_Pos_Num'), (0.66619665022083874, 'Dis_Doc_In_Pos_Num', 'Dis_Par_Med_Staf_In_Pos_Num'), (0.66431064757189739, 'Mat_An_Chil_Wel_Cen_Par_Med_Staf_In_Pos_Num', 'TB_Clin_Par_Med_Par_Med_Staf_Tot_Stren_Num'), (0.66198652932404967, 'Dis_Doc_In_Pos_Num', 'Dis_Par_Med_Staf_Tot_Stren_Num'), (0.65890980557838918, 'Dis_Doc_Tot_Stren_Num', 'Dis_Par_Med_Staf_Tot_Stren_Num'), (0.65816393312794574, 'Pow_Sup_For_Al_User_Win_Oc_Mar_per_day_in_Hour', 'Pow_Sup_For_Com_Us_Win_Oc_Mar_per_day_in_Hour'), (0.65125700569970268, 'Fam_Wel_Cen_Doc_Tot_Stren_Num', 'Fam_Wel_Cen_Num'), (0.65077256582727427, 'Dis_Doc_Tot_Stren_Num', 'Dis_Par_Med_Staf_In_Pos_Num'), (0.63960706286194935, 'Mat_An_Chil_Wel_Cen_Par_Med_Staf_Tot_Stren_Num', 'TB_Clin_Par_Med_Par_Med_Staf_Tot_Stren_Num'), (0.63857823177932527, 'Pow_Sup_For_Al_User_Win_Oc_Mar_per_day_in_Hour', 'Pow_Sup_For_Com_Us_Sum_April_Sep_per_day_in_Hour'), (0.63771744799805907, 'Pow_Sup_For_Al_User_Sum_April_Sep_per_day_in_Hour', 'Pow_Sup_For_Com_Us_Sum_April_Sep_per_day_in_Hour'), (0.63685974602335471, 'Pow_Sup_For_Al_User_Sum_April_Sep_per_day_in_Hour', 'Pow_Sup_For_Com_Us_Win_Oc_Mar_per_day_in_Hour'), (0.63337626405887382, 'Fam_Wel_Cen_Num', 'Fam_Wel_Cen_Par_Med_Staf_Tot_Stren_Num'), (0.62353526671381643, 'Hos_Allop_Doc_In_Pos_Num', 'Hos_Allop_Num'), (0.62278437083923488, 'Priv_Sec_School_Num', 'Priv_Sen_Sec_School_Num'), (0.62149052894321655, 'Mat_An_Chil_Wel_Cen_Par_Med_Staf_Tot_Stren_Num', 'TB_Clin_Par_Med_Par_Med_Staf_In_Pos_Num'), (0.61512260761180682, 'Gov_Prim_School_Num', 'Tot_Hous'), (0.61385438807646298, 'Hos_Allop_Doc_Tot_Stren_Num', 'Hos_Allop_Num')]
    count = 0
    thresh = 1
    for score,field_1,field_2 in field_pairs:
        path = "JSONS/Ratio/Fact@{}@{}.json".format(field_1,field_2)
        print(field_1,field_2)
        if not (os.path.isfile(path)):
            print("==========================================================================================")
            s = NumericRatioFact(fields=[field_1,field_2], fileName=path, debug=DEBUG)
            s.partitions = partitions
            s.fuzzy_intersection()
            print("==========================================================================================")
        path = "JSONS/Ratio/Fact@{}@{}.json".format(field_1,field_2)
        print("==========================================================================================")
        s = NumericRatioFact(fields=[field_1,field_2], fileName=path, debug=DEBUG)
        s.partitions = partitions
        s.fuzzy_intersection()
        print("==========================================================================================")
        count += 1
        perc = count / len(field_pairs) * 100
        if perc > thresh:
            print("{}% completed".format(perc))
            thresh += 1

#gen_simple()
gen_semantic()
#gen_ratio()