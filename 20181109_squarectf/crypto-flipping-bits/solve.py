from crypto_commons.rsa.rsa_commons import extended_gcd
from Crypto.Util.number import *

ct_13 = 13981765388145083997703333682243956434148306954774120760845671024723583618341148528952063316653588928138430524040717841543528568326674293677228449651281422762216853098529425814740156575513620513245005576508982103360592761380293006244528169193632346512170599896471850340765607466109228426538780591853882736654
ct_15 = 79459949016924442856959059325390894723232586275925931898929445938338123216278271333902062872565058205136627757713051954083968874644581902371182266588247653857616029881453100387797111559677392017415298580136496204898016797180386402171968931958365160589774450964944023720256848731202333789801071962338635072065
n = 103109065902334620226101162008793963504256027939117020091876799039690801944735604259018655534860183205031069083254290258577291605287053538752280231959857465853228851714786887294961873006234153079187216285516823832102424110934062954272346111907571393964363630079343598511602013316604641904852018969178919051627

def _pow(ct, power):
	if power < 0:
		return pow(inverse(ct, n), -power, n)
	return pow(ct, power, n)

_, exp_13, exp_15 = extended_gcd(13, 15)
flag = _pow(ct_13, exp_13)*_pow(ct_15, exp_15)
print(long_to_bytes(flag%n))
#flag-54d3db5c1efcd7afa579c37bcb560ae0
 
