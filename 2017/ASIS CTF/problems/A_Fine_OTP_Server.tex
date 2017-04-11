%% LyX 2.2.2 created this file.  For more info, see http://www.lyx.org/.
%% Do not edit unless you really know what you are doing.
\documentclass[english]{article}
\usepackage[T1]{fontenc}
\usepackage[latin9]{inputenc}

\makeatletter
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Textclass specific LaTeX commands.
\newenvironment{lyxcode}
{\par\begin{list}{}{
\setlength{\rightmargin}{\leftmargin}
\setlength{\listparindent}{0pt}% needed for AMS classes
\raggedright
\setlength{\itemsep}{0pt}
\setlength{\parsep}{0pt}
\normalfont\ttfamily}%
 \item[]}
{\end{list}}

\makeatother

\usepackage{babel}
\begin{document}

\title{A Fine OTP Server}
\maketitle
\begin{itemize}
\item Cryptography, RSA
\item 79 points
\item Connect to OTP generator server, and try to find one OTP. nc 66.172.27.77
35156 

So in the OTP server, they give us a RSA modulus, an encrypted message,
and the function used to encrypt the message. The One Time Pads are
encrypted with: 

\end{itemize}
\begin{lyxcode}
def~gen\_otps():

template\_phrase~=~'Welcome,~dear~customer,~the~secret~passphrase~for~today~is:~'

~~~~OTP\_1~=~template\_phrase~+~gen\_passphrase(18)

~~~~OTP\_2~=~template\_phrase~+~gen\_passphrase(18)

~~~~otp\_1~=~bytes\_to\_long(OTP\_1)

~~~~otp\_2~=~bytes\_to\_long(OTP\_2)

~~~~nbit,~e~=~2048,~3~~~~~

	privkey~=~RSA.generate(nbit,~e~=~e)

~~~~pubkey~~=~privkey.publickey().exportKey()

~~~~n~=~getattr(privkey.key,~'n')

~~~~r~=~otp\_2~-~otp\_1

	if~r~<~0:

~~~~~~~~r~=~-r

	IMP~=~n~-~r{*}{*}(e{*}{*}2)

~~~~if~IMP~>~0:

~~~~	c\_1~=~pow(otp\_1,~e,~n)

~~~~	c\_2~=~pow(otp\_2,~e,~n)

~~~~return~pubkey,~OTP\_1{[}-18:{]},~OTP\_2{[}-18:{]},~c\_1,~c\_2~
\end{lyxcode}
The template phrase is 60 bytes long, and OTP\_1 which includes the
passphrase is 78 bytes, or 624 bits long. $OTP_{1}^{3}$is on the
order of $624*3$ bits long. $624*3=1872<2048$ bits, so this doesn't
wrap around the modulus! We just need to take the cubed root of one
of the given messages, and provide that to the server to get the flag.
\begin{lyxcode}
valar@valardev-Vostro-3460-mint~\textasciitilde{}~\$~nc~66.172.27.77~35156

|-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-|

|~Welcome~to~the~S3cure~OTP~Generator~|

|-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-|

|~Guess~the~OTP~and~get~the~nice~flag!|

|~Options:

~	{[}F{]}irst~encrypted~OTP

~	{[}S{]}econd~encrypted~OTP

~	{[}G{]}uess~the~OTP

~	{[}P{]}ublic~key

~	{[}E{]}ncryption~function

~	{[}Q{]}uit

P

the~public~key~is:

-{}-{}-{}-{}-BEGIN~PUBLIC~KEY-{}-{}-{}-{}-

MIIBIDANBgkqhkiG9w0BAQEFAAOCAQ0AMIIBCAKCAQEAvdBapg5SXCJHVikgokU0~c0LA67ftF9ZhIrqSETuq3N9ENeyJ8JJ2k4Yhd/6KSAmpeeKBBtCsdGRNTp9Fr0C3~UHHoilQNcY90nemQM9rXvqbHxv1jxqwzXzaa+PMIpYS1L4SuZCS6pg0EHyKyh8yA~hn0bYs++29n3JC3qMZTuUk9qaqmESXYN4h3E+7iagPQSlBOOf7j9oDRr+1xWLy6p~YhdGP5T9D0OLRK1YxtKxfKf2CNcbpmSQbWZsDNNf6XLE/bY/W2cqzLYM/kqelMUW~zCEkDkAB8rbqNMew3vXKPkzAutjOAgHHXyMki7drh69Iqh/PwUdEkFGVJM6qDTlV

nQIBAw==

-{}-{}-{}-{}-END~PUBLIC~KEY-{}-{}-{}-{}-

S~13424849164527521403756445050870196571038349263738328860728317613249912394547060932323343839684520029298203039106900245311207700034998334716959147080496357763457295947526957049778372756495200446608399891341545104439044387558803483395758936347236422777032750389168685961215888900831895812978537767135180444146730600624258885143451110857613987242815230302366387575914921806179951025936110822860493612676495094084562385780429368251618285138710394367778529362284103719513422256240065550184346443798331957264278917052649310159470104960346812700994655607599455558277625

Now~if~we~just~take~the~cubed~root~in~python,~with~the~following:

>\textcompwordmark{}>\textcompwordmark{}>~import~gmpy

>\textcompwordmark{}>\textcompwordmark{}>~S~=~13424849164527521403756445050870196571038349263738328860728317613249912394547060932323343839684520029298203039106900245311207700034998334716959147080496357763457295947526957049778372756495200446608399891341545104439044387558803483395758936347236422777032750389168685961215888900831895812978537767135180444146730600624258885143451110857613987242815230302366387575914921806179951025936110822860493612676495094084562385780429368251618285138710394367778529362284103719513422256240065550184346443798331957264278917052649310159470104960346812700994655607599455558277625~>\textcompwordmark{}>\textcompwordmark{}>~gmpy.root(S,3)~(mpz(23766750386011171096524965335062551726344030679891013787685943574919990535673615479694411579744947646169980809461874073987449785044052175643595830657866834651236910043569261364887415705705L),~1)

>\textcompwordmark{}>\textcompwordmark{}>~a~=~23766750386011171096524965335062551726344030679891013787685943574919990535673615479694411579744947646169980809461874073987449785044052175643595830657866834651236910043569261364887415705705L

>\textcompwordmark{}>\textcompwordmark{}>~import~binascii

>\textcompwordmark{}>\textcompwordmark{}>~binascii.unhexlify(hex(a){[}2:-1{]})

'Welcome,~dear~customer,~the~secret~passphrase~for~today~is:~UEcAoQ9pGZ16DCWPPi'
\end{lyxcode}
If we enter UEcAoQ9pGZ16DCWPPi into our netcat session, we get our
flag: 

ASIS\{<some random hex here>\}
\end{document}
