from sys import argv

script, filename1, filename2 = argv

txt = open(filename1)

txt2 = open(filename2, "w")

node_dict = {'BB18NP' : 1,'BB54EA' : 2,'BB55QE' : 3,'BB54QB' : 4,'BB54QW' : 5,'BB55BU' : 6,'BB56PN' : 7,'BB52LF' : 8,'BB98NW' : 9,'BB99BY' : 10,'BB103FB' : 11,'BB88DH' : 12,'PR77AE' : 13,'PR77AQ' : 14,'PR77BG' : 15,'BB90JR' : 16,'PR71BS' : 17,'BB103RH' : 18,'PR73FA' : 19,'PR73EF' : 20,'BL23BS' : 21,'BL84HJ' : 22,'BL97HZ' : 23,'BL09XG' : 24,'BL83AG' : 25,'BL22JR' : 26,'OL102TT' : 27,'WN60TD' : 28,'BL53WG' : 29,'PR73RJ' : 30,'BL22TF' : 31,'BL70HF' : 32,'BL66EE' : 33,'WN69RN' : 34,'PR75TW' : 35,'BL81JT' : 36,'BL17JB' : 37,'WN68HE' : 38,'WN60LF' : 39,'BL82RB' : 40,'BL95DL' : 41,'BL53UT' : 42,'BL26DQ' : 43,'BL97RR' : 44,'BL53YF' : 45,'BL53UA' : 46,'BL18RL' : 47,'BL16HY' : 48,'WN21XE' : 49,'BB185RS' : 50,'BL67QY' : 51,'PR69LZ' : 52,'OL104AT' : 53,'OL101DL' : 54,'BL16NP' : 55,'M262QJ' : 56,'BL16DH' : 57,'WN21RN' : 58,'BL18SF' : 59,'BL82BU' : 60,'M97HQ' : 61,'M469HL' : 62,'BL18SA' : 63,'WN60UA' : 64,'BL52BN' : 65,'WN21DY' : 66,'OL101FP' : 67,'OL101FQ' : 68,'BL64HS' : 69,'BL14DS' : 70,'BL67BL' : 71,'OL98RL' : 72,'OL101RN' : 73,'M389QX' : 74,'BL35LN' : 75,'BL52JS' : 76,'OL98BQ' : 77,'OL98PH' : 78,'M280NG' : 79,'OL99DT' : 80,'M246EH' : 81,'BL52DW' : 82,'OL98LW' : 83,'WN49HH' : 84,'OL113NN' : 85,'M98RN' : 86,'BL40BG' : 87,'M282SQ' : 88,'OL145SQ' : 89,'WN40SY' : 90,'M270NG' : 91,'M270JN' : 92,'M264NG' : 93,'M97FZ' : 94,'M359HP' : 95,'M389LU' : 96,'BL48JE' : 97,'M275WW' : 98,'M97GE' : 99,'M242UJ' : 100,'WN67NB' : 101,'BL32TD' : 102,'M307BU' : 103,'M279BA' : 104,'OL112YB' : 105,'WN67HL' : 106,'M74XN' : 107,'OL96JU' : 108,'M73BL' : 109,'OL98QW' : 110,'WN13PP' : 111,'M275NH' : 112,'OL81HB' : 113,'BL31JP' : 114,'M359UJ' : 115,'WN23JQ' : 116,'OL165BW' : 117,'WN13YB' : 118,'WN34HY' : 119,'WN36LT' : 120,'WN36TJ' : 121,'OL162DZ' : 122,'M263AB' : 123,'M94FU' : 124,'WN23UD' : 125,'M308DA' : 126,'M71ZN' : 127,'M88DE' : 128,'OL126HT' : 129,'OL25HF' : 130,'WN24TJ' : 131,'WN75NZ' : 132,'M401PJ' : 133,'WN75SX' : 134,'M350PG' : 135,'OL26UA' : 136,'OL162LZ' : 137,'WN35HA' : 138,'M342RJ' : 139,'M409PQ' : 140,'M71NF' : 141,'WN36LY' : 142,'M298TD' : 143,'M300SW' : 144,'M417AW' : 145,'M300NF' : 146,'OL13UB' : 147,'M242TN' : 148,'OL66TN' : 149,'WN74BP' : 150,'OL128QT' : 151,'OL13EU' : 152,'M31EY' : 153,'OL26SW' : 154,'M342JN' : 155,'M298AZ' : 156,'OL129XB' : 157,'OL162TL' : 158,'OL129PU' : 159,'OL69QA' : 160,'M329HA' : 161,'M342EW' : 162,'M418WY' : 163,'WN74UB' : 164,'M320EB' : 165,'M437UX' : 166,'WN72HU' : 167,'SK144FZ' : 168,'WN74BJ' : 169,'SK151UR' : 170,'M297EB' : 171,'M329HR' : 172,'SK145GU' : 173,'OL27DR' : 174,'OL14DA' : 175,'M329WA' : 176,'WN24AQ' : 177,'M419NJ' : 178,'SK151DY' : 179,'OL82JJ' : 180,'OL42UZ' : 181,'M446DU' : 182,'SK141QF' : 183,'M334QN' : 184,'M332PJ' : 185,'OL69DE' : 186,'M446DS' : 187,'M416PH' : 188,'M297GF' : 189,'WN25TP' : 190,'OL82EN' : 191,'SK30LU' : 192,'OL45EB' : 193,'SK58LG' : 194,'M224NR' : 195,'OL43JW' : 196,'SK153DP' : 197,'OL68XS' : 198,'M113DH' : 199,'SK148LR' : 200,'SK25DB' : 201,'SK45EH' : 202,'SK153EJ' : 203,'SK43HL' : 204,'M217FZ' : 205,'M147LG' : 206,'M147EQ' : 207,'SK43BG' : 208,'SK44HF' : 209,'SK27NA' : 210,'OL59SA' : 211,'OL59PB' : 212,'SK38PJ' : 213,'M201AS' : 214,'WA145YH' : 215,'SK83AG' : 216,'SK73DQ' : 217,'M220HH' : 218,'SK131EF' : 219,'WA158EF' : 220,'SK138EL' : 221,'SK75QP' : 222,'WA142ES' : 223,'WA169BX' : 224,'SK92PR' : 225,'SK96EJ' : 226,'WA168UJ' : 227}


for line in txt:
	# clean up the line and put it all in buffer
	line_arr = line.split(" ")
	#print line_arr
	cur_write_buff = line_arr[0] + " " + line_arr[1] + " " + line_arr[3]
	txt2.write(cur_write_buff)

'''
for line in txt:
	# clean up the line and put it all in buffer, 
	line_arr = line.split(" ")
	txt2.write(line_arr[0] + "\n")
'''

'''
i = 1
txt2.write("{")

for line in txt:
	# clean up the line and put it all in buffer, 
	line_arr = line.split("\n")
	txt2.write( "'" + line_arr[0] + "'" + " : " + str(i) + ",")
	i += 1

txt2.write("}")
'''

'''
	reading nodes_dict_coordinates
'''
'''
for line in txt:
	line_arr = line.split(" ")
	cur_write_buff = str(node_dict[str(line_arr[0])]) + " " + str(line_arr[7]) + " " + str(line_arr[8])
	txt2.write(cur_write_buff)
'''

print "Done reading the file. Bye now.."

quit()