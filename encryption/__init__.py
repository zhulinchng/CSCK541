"""Package installation file for the encryption package."""
import rsa
from .keygen import generate_keys, save_keys, load_priv_key, load_pub_key
from .cipher import encrypt, decrypt
__version__ = '0.3.0'
RSA_N = 19016607391604318237238985071154538845729314874533314886750294083273480587553854814511478026514219972610490249199310571041811639027786022611100474792456943767371838805379794641824088701247276698786610068715740538953101035308234577091250078134168174953976117195938121989763425866582218583331140663557782120964630006935670450949021031201086118199433502990130813537475144219377945835060653039718157191125814458594471035215985235335781369515915678940984016170234468507917100786320860266277598874903840766464470295635386289796210190957827238571615015278593099584044403747530613451891515043227894768246636499283164390271139
RSA_E = 65537
RSA_D = 8736317123860152486180193822151164312788473873421869243485021503260722241330415807182379120531762743722731288018872433479208154597381350516120864474286184337824912991933943529243628219435631884997287882400682303840578085219957072296006185093360016654932525695947403403692528281597531731798248472773822546644672637188525261540933055882188250886753457445794773645323362022762183146126368461059135921871971526742752777698178974139780926778960773472228056470511162081215015647806003541925143309728355146612314543020018346981648771235922197834078648736827115154612667921131920288305902858113413930172395415963995405809089
RSA_P = 2397134921605415788201462249062902602788517190727893267098219222668274214130560415956378849857324878015826408852960086667149530053767308431921484159375794665028798297357903288576603134256203315842191713985555263168212831521086852114203069664345442241349987965741867998203911118199727074850337581039802590098566454235047637195563
RSA_Q = 7933056758802906124265412704598563627658837108122158323966867945435906767228028492361069663162678192593026106083121586656355879124405350980311638039744829831311336231583920875264432165882325747095618686578877522904445332465996901110506660577642723038787545482272836388129883761004792450153
EXAMPLE_PUB_KEY = rsa.PublicKey(RSA_N, RSA_E)
EXAMPLE_PRIV_KEY = rsa.PrivateKey(RSA_N, RSA_E, RSA_D, RSA_P, RSA_Q)
