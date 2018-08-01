#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from __future__ import unicode_literals

def unicode2bamini(input_text):
    # input_text = input_text.replace(','.encode("utf-8").decode("utf-8"), ">")
    input_text = input_text.replace('ஜௌ'.encode("utf-8").decode("utf-8"), "n\[s")
    input_text = input_text.replace('ஜோ'.encode("utf-8").decode("utf-8"), "N\[h")
    input_text = input_text.replace('ஜொ'.encode("utf-8").decode("utf-8"), "n\[h")
    input_text = input_text.replace('ஜா'.encode("utf-8").decode("utf-8"), "\[h")
    input_text = input_text.replace('ஜி'.encode("utf-8").decode("utf-8"), "\[p")
    input_text = input_text.replace('ஜீ'.encode("utf-8").decode("utf-8"), "\[P")
    input_text = input_text.replace('ஜு'.encode("utf-8").decode("utf-8"), "\[{")
    input_text = input_text.replace('ஜூ'.encode("utf-8").decode("utf-8"), "\[_")
    input_text = input_text.replace('ஜெ'.encode("utf-8").decode("utf-8"), "n\[")
    input_text = input_text.replace('ஜே'.encode("utf-8").decode("utf-8"), "N\[")
    input_text = input_text.replace('ஜை'.encode("utf-8").decode("utf-8"), "i\[")
    input_text = input_text.replace('ஜ்'.encode("utf-8").decode("utf-8"), "\[;")
    input_text = input_text.replace('ஜ'.encode("utf-8").decode("utf-8"), "\[")

    input_text = input_text.replace('கௌ'.encode("utf-8").decode("utf-8"), "nfs")
    input_text = input_text.replace('கோ'.encode("utf-8").decode("utf-8"), "Nfh")
    input_text = input_text.replace('கொ'.encode("utf-8").decode("utf-8"), "nfh")
    input_text = input_text.replace('கா'.encode("utf-8").decode("utf-8"), "fh")
    input_text = input_text.replace('கி'.encode("utf-8").decode("utf-8"), "fp")
    input_text = input_text.replace('கீ'.encode("utf-8").decode("utf-8"), "fP")
    input_text = input_text.replace('கு'.encode("utf-8").decode("utf-8"), "F")
    input_text = input_text.replace('கூ'.encode("utf-8").decode("utf-8"), "$")
    input_text = input_text.replace('கெ'.encode("utf-8").decode("utf-8"), "nf")
    input_text = input_text.replace('கே'.encode("utf-8").decode("utf-8"), "Nf")
    input_text = input_text.replace('கை'.encode("utf-8").decode("utf-8"), "if")
    input_text = input_text.replace('க்'.encode("utf-8").decode("utf-8"), "f;")
    input_text = input_text.replace('க'.encode("utf-8").decode("utf-8"), "f")

    input_text = input_text.replace('ஙௌ'.encode("utf-8").decode("utf-8"), "nqs")
    input_text = input_text.replace('ஙோ'.encode("utf-8").decode("utf-8"), "Nqh")
    input_text = input_text.replace('ஙொ'.encode("utf-8").decode("utf-8"), "nqh")
    input_text = input_text.replace('ஙா'.encode("utf-8").decode("utf-8"), "qh")
    input_text = input_text.replace('ஙி'.encode("utf-8").decode("utf-8"), "qp")
    input_text = input_text.replace('ஙீ'.encode("utf-8").decode("utf-8"), "qP")
    input_text = input_text.replace('ஙு'.encode("utf-8").decode("utf-8"), "*")
    input_text = input_text.replace('ஙூ'.encode("utf-8").decode("utf-8"), "*")
    input_text = input_text.replace('ஙெ'.encode("utf-8").decode("utf-8"), "nq")
    input_text = input_text.replace('ஙே'.encode("utf-8").decode("utf-8"), "Nq")
    input_text = input_text.replace('ஙை'.encode("utf-8").decode("utf-8"), "iq")
    input_text = input_text.replace('ங்'.encode("utf-8").decode("utf-8"), "q;")
    input_text = input_text.replace('ங'.encode("utf-8").decode("utf-8"), "q")

    input_text = input_text.replace('சௌ'.encode("utf-8").decode("utf-8"), "nrs")
    input_text = input_text.replace('சோ'.encode("utf-8").decode("utf-8"), "Nrh")
    input_text = input_text.replace('சொ'.encode("utf-8").decode("utf-8"), "nrh")
    input_text = input_text.replace('சா'.encode("utf-8").decode("utf-8"), "rh")
    input_text = input_text.replace('சி'.encode("utf-8").decode("utf-8"), "rp")
    input_text = input_text.replace('சீ'.encode("utf-8").decode("utf-8"), "rP")
    input_text = input_text.replace('சு'.encode("utf-8").decode("utf-8"), "R")
    input_text = input_text.replace('சூ'.encode("utf-8").decode("utf-8"), "R+")
    input_text = input_text.replace('செ'.encode("utf-8").decode("utf-8"), "nr")
    input_text = input_text.replace('சே'.encode("utf-8").decode("utf-8"), "Nr")
    input_text = input_text.replace('சை'.encode("utf-8").decode("utf-8"), "ir")
    input_text = input_text.replace('ச்'.encode("utf-8").decode("utf-8"), "r;")
    input_text = input_text.replace('ச'.encode("utf-8").decode("utf-8"), "r")

    input_text = input_text.replace('ஞௌ'.encode("utf-8").decode("utf-8"), "nQs")
    input_text = input_text.replace('ஞோ'.encode("utf-8").decode("utf-8"), "NQh")
    input_text = input_text.replace('ஞொ'.encode("utf-8").decode("utf-8"), "nQh")
    input_text = input_text.replace('ஞா'.encode("utf-8").decode("utf-8"), "Qh")
    input_text = input_text.replace('ஞி'.encode("utf-8").decode("utf-8"), "Qp")
    input_text = input_text.replace('ஞீ'.encode("utf-8").decode("utf-8"), "QP")
    input_text = input_text.replace('ஞு'.encode("utf-8").decode("utf-8"), "*")
    input_text = input_text.replace('ஞூ'.encode("utf-8").decode("utf-8"), "*")
    input_text = input_text.replace('ஞெ'.encode("utf-8").decode("utf-8"), "nQ")
    input_text = input_text.replace('ஞே'.encode("utf-8").decode("utf-8"), "NQ")
    input_text = input_text.replace('ஞை'.encode("utf-8").decode("utf-8"), "iQ")
    input_text = input_text.replace('ஞ்'.encode("utf-8").decode("utf-8"), "Q;")
    input_text = input_text.replace('ஞ'.encode("utf-8").decode("utf-8"), "Q")

    input_text = input_text.replace('டௌ'.encode("utf-8").decode("utf-8"), "nls")
    input_text = input_text.replace('டோ'.encode("utf-8").decode("utf-8"), "Nlh")
    input_text = input_text.replace('டொ'.encode("utf-8").decode("utf-8"), "nlh")
    input_text = input_text.replace('டா'.encode("utf-8").decode("utf-8"), "lh")
    input_text = input_text.replace('டி'.encode("utf-8").decode("utf-8"), "b")
    input_text = input_text.replace('டீ'.encode("utf-8").decode("utf-8"), "B")
    input_text = input_text.replace('டு'.encode("utf-8").decode("utf-8"), "L")
    input_text = input_text.replace('டூ'.encode("utf-8").decode("utf-8"), "^")
    input_text = input_text.replace('டெ'.encode("utf-8").decode("utf-8"), "nl")
    input_text = input_text.replace('டே'.encode("utf-8").decode("utf-8"), "Nl")
    input_text = input_text.replace('டை'.encode("utf-8").decode("utf-8"), "il")
    input_text = input_text.replace('ட்'.encode("utf-8").decode("utf-8"), "l;")
    input_text = input_text.replace('ட'.encode("utf-8").decode("utf-8"), "l")

    input_text = input_text.replace('ணௌ'.encode("utf-8").decode("utf-8"), "nzs")
    input_text = input_text.replace('ணோ'.encode("utf-8").decode("utf-8"), "Nzh")
    input_text = input_text.replace('ணொ'.encode("utf-8").decode("utf-8"), "nzh")
    input_text = input_text.replace('ணா'.encode("utf-8").decode("utf-8"), "zh")
    input_text = input_text.replace('ணி'.encode("utf-8").decode("utf-8"), "zp")
    input_text = input_text.replace('ணீ'.encode("utf-8").decode("utf-8"), "zP")
    input_text = input_text.replace('ணு'.encode("utf-8").decode("utf-8"), "Z")
    input_text = input_text.replace('ணூ'.encode("utf-8").decode("utf-8"), "Z}")
    input_text = input_text.replace('ணெ'.encode("utf-8").decode("utf-8"), "nz")
    input_text = input_text.replace('ணே'.encode("utf-8").decode("utf-8"), "Nz")
    input_text = input_text.replace('ணை'.encode("utf-8").decode("utf-8"), "iz")
    input_text = input_text.replace('ண்'.encode("utf-8").decode("utf-8"), "z;")
    input_text = input_text.replace('ண'.encode("utf-8").decode("utf-8"), "z")

    input_text = input_text.replace('தௌ'.encode("utf-8").decode("utf-8"), "njs")
    input_text = input_text.replace('தோ'.encode("utf-8").decode("utf-8"), "Njh")
    input_text = input_text.replace('தொ'.encode("utf-8").decode("utf-8"), "njh")
    input_text = input_text.replace('தா'.encode("utf-8").decode("utf-8"), "jh")
    input_text = input_text.replace('தி'.encode("utf-8").decode("utf-8"), "jp")
    input_text = input_text.replace('தீ'.encode("utf-8").decode("utf-8"), "jP")
    input_text = input_text.replace('து'.encode("utf-8").decode("utf-8"), "J")
    input_text = input_text.replace('தூ'.encode("utf-8").decode("utf-8"), "J}")
    input_text = input_text.replace('தெ'.encode("utf-8").decode("utf-8"), "nj")
    input_text = input_text.replace('தே'.encode("utf-8").decode("utf-8"), "Nj")
    input_text = input_text.replace('தை'.encode("utf-8").decode("utf-8"), "ij")
    input_text = input_text.replace('த்'.encode("utf-8").decode("utf-8"), "j;")
    input_text = input_text.replace('த'.encode("utf-8").decode("utf-8"), "j")

    input_text = input_text.replace('நௌ'.encode("utf-8").decode("utf-8"), "nes")
    input_text = input_text.replace('நோ'.encode("utf-8").decode("utf-8"), "Neh")
    input_text = input_text.replace('நொ'.encode("utf-8").decode("utf-8"), "neh")
    input_text = input_text.replace('நா'.encode("utf-8").decode("utf-8"), "eh")
    input_text = input_text.replace('நி'.encode("utf-8").decode("utf-8"), "ep")
    input_text = input_text.replace('நீ'.encode("utf-8").decode("utf-8"), "eP")
    input_text = input_text.replace('நு'.encode("utf-8").decode("utf-8"), "E")
    input_text = input_text.replace('நூ'.encode("utf-8").decode("utf-8"), "E}")
    input_text = input_text.replace('நெ'.encode("utf-8").decode("utf-8"), "ne")
    input_text = input_text.replace('நே'.encode("utf-8").decode("utf-8"), "Ne")
    input_text = input_text.replace('நை'.encode("utf-8").decode("utf-8"), "ie")
    input_text = input_text.replace('ந்'.encode("utf-8").decode("utf-8"), "e;")
    input_text = input_text.replace('ந'.encode("utf-8").decode("utf-8"), "e")

    input_text = input_text.replace('னௌ'.encode("utf-8").decode("utf-8"), "nds")
    input_text = input_text.replace('னோ'.encode("utf-8").decode("utf-8"), "Ndh")
    input_text = input_text.replace('னொ'.encode("utf-8").decode("utf-8"), "ndh")
    input_text = input_text.replace('னா'.encode("utf-8").decode("utf-8"), "dh")
    input_text = input_text.replace('னி'.encode("utf-8").decode("utf-8"), "dp")
    input_text = input_text.replace('னீ'.encode("utf-8").decode("utf-8"), "dP")
    input_text = input_text.replace('னு'.encode("utf-8").decode("utf-8"), "D")
    input_text = input_text.replace('னூ'.encode("utf-8").decode("utf-8"), "D}")
    input_text = input_text.replace('னெ'.encode("utf-8").decode("utf-8"), "nd")
    input_text = input_text.replace('னே'.encode("utf-8").decode("utf-8"), "Nd")
    input_text = input_text.replace('னை'.encode("utf-8").decode("utf-8"), "id")
    input_text = input_text.replace('ன்'.encode("utf-8").decode("utf-8"), "d;")
    input_text = input_text.replace('ன'.encode("utf-8").decode("utf-8"), "d")


    input_text = input_text.replace('பௌ'.encode("utf-8").decode("utf-8"), "ngs")
    input_text = input_text.replace('போ'.encode("utf-8").decode("utf-8"), "Ngh")
    input_text = input_text.replace('பொ'.encode("utf-8").decode("utf-8"), "ngh")
    input_text = input_text.replace('பா'.encode("utf-8").decode("utf-8"), "gh")
    input_text = input_text.replace('பி'.encode("utf-8").decode("utf-8"), "gp")
    input_text = input_text.replace('பீ'.encode("utf-8").decode("utf-8"), "gP")
    input_text = input_text.replace('பு'.encode("utf-8").decode("utf-8"), "G")
    input_text = input_text.replace('பூ'.encode("utf-8").decode("utf-8"), "G+")
    input_text = input_text.replace('பெ'.encode("utf-8").decode("utf-8"), "ng")
    input_text = input_text.replace('பே'.encode("utf-8").decode("utf-8"), "Ng")
    input_text = input_text.replace('பை'.encode("utf-8").decode("utf-8"), "ig")
    input_text = input_text.replace('ப்'.encode("utf-8").decode("utf-8"), "g;")
    input_text = input_text.replace('ப'.encode("utf-8").decode("utf-8"), "g")


    input_text = input_text.replace('மௌ'.encode("utf-8").decode("utf-8"), "nks")
    input_text = input_text.replace('மோ'.encode("utf-8").decode("utf-8"), "Nkh")
    input_text = input_text.replace('மொ'.encode("utf-8").decode("utf-8"), "nkh")
    input_text = input_text.replace('மா'.encode("utf-8").decode("utf-8"), "kh")
    input_text = input_text.replace('மி'.encode("utf-8").decode("utf-8"), "kp")
    input_text = input_text.replace('மீ'.encode("utf-8").decode("utf-8"), "kP")
    input_text = input_text.replace('மு'.encode("utf-8").decode("utf-8"), "K")
    input_text = input_text.replace('மூ'.encode("utf-8").decode("utf-8"), "%")
    input_text = input_text.replace('மெ'.encode("utf-8").decode("utf-8"), "nk")
    input_text = input_text.replace('மே'.encode("utf-8").decode("utf-8"), "Nk")
    input_text = input_text.replace('மை'.encode("utf-8").decode("utf-8"), "ik")
    input_text = input_text.replace('ம்'.encode("utf-8").decode("utf-8"), "k;")
    input_text = input_text.replace('ம'.encode("utf-8").decode("utf-8"), "k")


    input_text = input_text.replace('யௌ'.encode("utf-8").decode("utf-8"), "nas")
    input_text = input_text.replace('யோ'.encode("utf-8").decode("utf-8"), "Nah")
    input_text = input_text.replace('யொ'.encode("utf-8").decode("utf-8"), "nah")
    input_text = input_text.replace('யா'.encode("utf-8").decode("utf-8"), "ah")
    input_text = input_text.replace('யி'.encode("utf-8").decode("utf-8"), "ap")
    input_text = input_text.replace('யீ'.encode("utf-8").decode("utf-8"), "aP")
    input_text = input_text.replace('யு'.encode("utf-8").decode("utf-8"), "A")
    input_text = input_text.replace('யூ'.encode("utf-8").decode("utf-8"), "A+")
    input_text = input_text.replace('யெ'.encode("utf-8").decode("utf-8"), "na")
    input_text = input_text.replace('யே'.encode("utf-8").decode("utf-8"), "Na")
    input_text = input_text.replace('யை'.encode("utf-8").decode("utf-8"), "ia")
    input_text = input_text.replace('ய்'.encode("utf-8").decode("utf-8"), "a;")
    input_text = input_text.replace('ய'.encode("utf-8").decode("utf-8"), "a")

    input_text = input_text.replace('ரௌ'.encode("utf-8").decode("utf-8"), "nus")
    input_text = input_text.replace('ரோ'.encode("utf-8").decode("utf-8"), "Nuh")
    input_text = input_text.replace('ரொ'.encode("utf-8").decode("utf-8"), "nuh")
    input_text = input_text.replace('ரா'.encode("utf-8").decode("utf-8"), "uh")
    input_text = input_text.replace('ரி'.encode("utf-8").decode("utf-8"), "up")
    input_text = input_text.replace('ரீ'.encode("utf-8").decode("utf-8"), "uP")
    input_text = input_text.replace('ரு'.encode("utf-8").decode("utf-8"), "U")
    input_text = input_text.replace('ரூ'.encode("utf-8").decode("utf-8"), "\&")
    input_text = input_text.replace('ரெ'.encode("utf-8").decode("utf-8"), "nu")
    input_text = input_text.replace('ரே'.encode("utf-8").decode("utf-8"), "Nu")
    input_text = input_text.replace('ரை'.encode("utf-8").decode("utf-8"), "iu")
    input_text = input_text.replace('ர்'.encode("utf-8").decode("utf-8"), "u;")
    input_text = input_text.replace('ர'.encode("utf-8").decode("utf-8"), "u")


    input_text = input_text.replace('லௌ'.encode("utf-8").decode("utf-8"), "nys")
    input_text = input_text.replace('லோ'.encode("utf-8").decode("utf-8"), "Nyh")
    input_text = input_text.replace('லொ'.encode("utf-8").decode("utf-8"), "nyh")
    input_text = input_text.replace('லா'.encode("utf-8").decode("utf-8"), "yh")
    input_text = input_text.replace('லி'.encode("utf-8").decode("utf-8"), "yp")
    input_text = input_text.replace('லீ'.encode("utf-8").decode("utf-8"), "yP")
    input_text = input_text.replace('லு'.encode("utf-8").decode("utf-8"), "Y")
    input_text = input_text.replace('லூ'.encode("utf-8").decode("utf-8"), "Y}")
    input_text = input_text.replace('லெ'.encode("utf-8").decode("utf-8"), "ny")
    input_text = input_text.replace('லே'.encode("utf-8").decode("utf-8"), "Ny")
    input_text = input_text.replace('லை'.encode("utf-8").decode("utf-8"), "iy")
    input_text = input_text.replace('ல்'.encode("utf-8").decode("utf-8"), "y;")
    input_text = input_text.replace('ல'.encode("utf-8").decode("utf-8"), "y")


    input_text = input_text.replace('ளௌ'.encode("utf-8").decode("utf-8"), "nss")
    input_text = input_text.replace('ளோ'.encode("utf-8").decode("utf-8"), "Nsh")
    input_text = input_text.replace('ளொ'.encode("utf-8").decode("utf-8"), "nsh")
    input_text = input_text.replace('ளா'.encode("utf-8").decode("utf-8"), "sh")
    input_text = input_text.replace('ளி'.encode("utf-8").decode("utf-8"), "sp")
    input_text = input_text.replace('ளீ'.encode("utf-8").decode("utf-8"), "sP")
    input_text = input_text.replace('ளு'.encode("utf-8").decode("utf-8"), "S")
    input_text = input_text.replace('ளூ'.encode("utf-8").decode("utf-8"), "Sh")
    input_text = input_text.replace('ளெ'.encode("utf-8").decode("utf-8"), "ns")
    input_text = input_text.replace('ளே'.encode("utf-8").decode("utf-8"), "Ns")
    input_text = input_text.replace('ளை'.encode("utf-8").decode("utf-8"), "is")
    input_text = input_text.replace('ள்'.encode("utf-8").decode("utf-8"), "s;")
    input_text = input_text.replace('ள'.encode("utf-8").decode("utf-8"), "s")

    input_text = input_text.replace('வௌ'.encode("utf-8").decode("utf-8"), "nts")
    input_text = input_text.replace('வோ'.encode("utf-8").decode("utf-8"), "Nth")
    input_text = input_text.replace('வொ'.encode("utf-8").decode("utf-8"), "nth")
    input_text = input_text.replace('வா'.encode("utf-8").decode("utf-8"), "th")
    input_text = input_text.replace('வி'.encode("utf-8").decode("utf-8"), "tp")
    input_text = input_text.replace('வீ'.encode("utf-8").decode("utf-8"), "tP")
    input_text = input_text.replace('வு'.encode("utf-8").decode("utf-8"), "T")
    input_text = input_text.replace('வூ'.encode("utf-8").decode("utf-8"), "T+")
    input_text = input_text.replace('வெ'.encode("utf-8").decode("utf-8"), "nt")
    input_text = input_text.replace('வே'.encode("utf-8").decode("utf-8"), "Nt")
    input_text = input_text.replace('வை'.encode("utf-8").decode("utf-8"), "it")
    input_text = input_text.replace('வ்'.encode("utf-8").decode("utf-8"), "t;")
    input_text = input_text.replace('வ'.encode("utf-8").decode("utf-8"), "t")


    input_text = input_text.replace('ழௌ'.encode("utf-8").decode("utf-8"), "nos")
    input_text = input_text.replace('ழோ'.encode("utf-8").decode("utf-8"), "Noh")
    input_text = input_text.replace('ழொ'.encode("utf-8").decode("utf-8"), "noh")
    input_text = input_text.replace('ழா'.encode("utf-8").decode("utf-8"), "oh")
    input_text = input_text.replace('ழி'.encode("utf-8").decode("utf-8"), "op")
    input_text = input_text.replace('ழீ'.encode("utf-8").decode("utf-8"), "oP")
    input_text = input_text.replace('ழு'.encode("utf-8").decode("utf-8"), "O")
    input_text = input_text.replace('ழூ'.encode("utf-8").decode("utf-8"), "*")
    input_text = input_text.replace('ழெ'.encode("utf-8").decode("utf-8"), "no")
    input_text = input_text.replace('ழே'.encode("utf-8").decode("utf-8"), "No")
    input_text = input_text.replace('ழை'.encode("utf-8").decode("utf-8"), "io")
    input_text = input_text.replace('ழ்'.encode("utf-8").decode("utf-8"), "o;")
    input_text = input_text.replace('ழ'.encode("utf-8").decode("utf-8"), "o")

    input_text = input_text.replace('றௌ'.encode("utf-8").decode("utf-8"), "nws")
    input_text = input_text.replace('றோ'.encode("utf-8").decode("utf-8"), "Nwh")
    input_text = input_text.replace('றொ'.encode("utf-8").decode("utf-8"), "nwh")
    input_text = input_text.replace('றா'.encode("utf-8").decode("utf-8"), "wh")
    input_text = input_text.replace('றி'.encode("utf-8").decode("utf-8"), "wp")
    input_text = input_text.replace('றீ'.encode("utf-8").decode("utf-8"), "wP")
    input_text = input_text.replace('று'.encode("utf-8").decode("utf-8"), "W")
    input_text = input_text.replace('றூ'.encode("utf-8").decode("utf-8"), "W}")
    input_text = input_text.replace('றெ'.encode("utf-8").decode("utf-8"), "nw")
    input_text = input_text.replace('றே'.encode("utf-8").decode("utf-8"), "Nw")
    input_text = input_text.replace('றை'.encode("utf-8").decode("utf-8"), "iw")
    input_text = input_text.replace('ற்'.encode("utf-8").decode("utf-8"), "w;")
    input_text = input_text.replace('ற'.encode("utf-8").decode("utf-8"), "w")

    input_text = input_text.replace('ஹௌ'.encode("utf-8").decode("utf-8"), "n`s")
    input_text = input_text.replace('ஹோ'.encode("utf-8").decode("utf-8"), "N`h")
    input_text = input_text.replace('ஹொ'.encode("utf-8").decode("utf-8"), "n`h")
    input_text = input_text.replace('ஹா'.encode("utf-8").decode("utf-8"), "`h")
    input_text = input_text.replace('ஹி'.encode("utf-8").decode("utf-8"), "`p")
    input_text = input_text.replace('ஹீ'.encode("utf-8").decode("utf-8"), "`P")
    input_text = input_text.replace('ஹு'.encode("utf-8").decode("utf-8"), "{`")
    input_text = input_text.replace('ஹூ'.encode("utf-8").decode("utf-8"), "`_")
    input_text = input_text.replace('ஹெ'.encode("utf-8").decode("utf-8"), "n`")
    input_text = input_text.replace('ஹே'.encode("utf-8").decode("utf-8"), "N`")
    input_text = input_text.replace('ஹை'.encode("utf-8").decode("utf-8"), "i`")
    input_text = input_text.replace('ஹ்'.encode("utf-8").decode("utf-8"), "`;")
    input_text = input_text.replace('ஹ'.encode("utf-8").decode("utf-8"), "`")

    input_text = input_text.replace('ஷௌ'.encode("utf-8").decode("utf-8"), "n\\s")
    input_text = input_text.replace('ஷோ'.encode("utf-8").decode("utf-8"), "N\\h")
    input_text = input_text.replace('ஷொ'.encode("utf-8").decode("utf-8"), "n\\h")
    input_text = input_text.replace('ஷா'.encode("utf-8").decode("utf-8"), "\\h")
    input_text = input_text.replace('ஷி'.encode("utf-8").decode("utf-8"), "\\p")
    input_text = input_text.replace('ஷீ'.encode("utf-8").decode("utf-8"), "\\P")
    input_text = input_text.replace('ஷு'.encode("utf-8").decode("utf-8"), "\{")
    input_text = input_text.replace('ஷூ'.encode("utf-8").decode("utf-8"), "\\\_")
    input_text = input_text.replace('ஷெ'.encode("utf-8").decode("utf-8"), "n\\")
    input_text = input_text.replace('ஷே'.encode("utf-8").decode("utf-8"), "N\\")
    input_text = input_text.replace('ஷை'.encode("utf-8").decode("utf-8"), "i\\")
    input_text = input_text.replace('ஷ்'.encode("utf-8").decode("utf-8"), "\\;")
    input_text = input_text.replace('ஷ'.encode("utf-8").decode("utf-8"), "\\")

    input_text = input_text.replace('ஸௌ'.encode("utf-8").decode("utf-8"), "n]s")
    input_text = input_text.replace('ஸோ'.encode("utf-8").decode("utf-8"), "N]h")
    input_text = input_text.replace('ஸொ'.encode("utf-8").decode("utf-8"), "n]h")
    input_text = input_text.replace('ஸா'.encode("utf-8").decode("utf-8"), "]h")
    input_text = input_text.replace('ஸி'.encode("utf-8").decode("utf-8"), "]p")
    input_text = input_text.replace('ஸீ'.encode("utf-8").decode("utf-8"), "]P")
    input_text = input_text.replace('ஸு'.encode("utf-8").decode("utf-8"), "]{")
    input_text = input_text.replace('ஸூ'.encode("utf-8").decode("utf-8"), "]_")
    input_text = input_text.replace('ஸெ'.encode("utf-8").decode("utf-8"), "n]")
    input_text = input_text.replace('ஸே'.encode("utf-8").decode("utf-8"), "N]")
    input_text = input_text.replace('ஸை'.encode("utf-8").decode("utf-8"), "i]")
    input_text = input_text.replace('ஸ்'.encode("utf-8").decode("utf-8"), "];")
    input_text = input_text.replace('ஸ'.encode("utf-8").decode("utf-8"), "]")

    input_text = input_text.replace('அ'.encode("utf-8").decode("utf-8"), "m")
    input_text = input_text.replace('ஆ'.encode("utf-8").decode("utf-8"), "M")
    input_text = input_text.replace('இ'.encode("utf-8").decode("utf-8"), ",")
    input_text = input_text.replace('ஈ'.encode("utf-8").decode("utf-8"), "<")
    input_text = input_text.replace('உ'.encode("utf-8").decode("utf-8"), "c")
    input_text = input_text.replace('ஊ'.encode("utf-8").decode("utf-8"), "C")
    input_text = input_text.replace('எ'.encode("utf-8").decode("utf-8"), "v")
    input_text = input_text.replace('ஏ'.encode("utf-8").decode("utf-8"), "V")
    input_text = input_text.replace('ஐ'.encode("utf-8").decode("utf-8"), "I")
    input_text = input_text.replace('ஒ'.encode("utf-8").decode("utf-8"), "x")
    input_text = input_text.replace('ஓ'.encode("utf-8").decode("utf-8"), "X")
    input_text = input_text.replace('ஔ'.encode("utf-8").decode("utf-8"), "xs")
    input_text = input_text.replace('ஃ'.encode("utf-8").decode("utf-8"), "\/")
    input_text = input_text.replace('ஸ்ரீ'.encode("utf-8").decode("utf-8"), "=")

    input_text = input_text.replace('வூ'.encode("utf-8").decode("utf-8"), "t+")
    input_text = input_text.replace('பூ'.encode("utf-8").decode("utf-8"), "G+")
    input_text = input_text.replace('யூ'.encode("utf-8").decode("utf-8"), "A+")
    input_text = input_text.replace('ஹு'.encode("utf-8").decode("utf-8"), "`{")
    input_text = input_text.replace('ஜு'.encode("utf-8").decode("utf-8"), "[{")
    input_text = input_text.replace('ஸு'.encode("utf-8").decode("utf-8"), "]{")
    input_text = input_text.replace('ஷு'.encode("utf-8").decode("utf-8"), "\{")
    input_text = input_text.replace('யூ'.encode("utf-8").decode("utf-8"), "A+")
    input_text = input_text.replace('ா'.encode("utf-8").decode("utf-8"), "h")
    input_text = input_text.replace('ெ'.encode("utf-8").decode("utf-8"), "n")
    input_text = input_text.replace('ே'.encode("utf-8").decode("utf-8"), "N")
    input_text = input_text.replace('ை'.encode("utf-8").decode("utf-8"), "i")
    input_text = input_text.replace('ு'.encode("utf-8").decode("utf-8"), "{")
    input_text = input_text.replace('ூ'.encode("utf-8").decode("utf-8"), "_")
    input_text = input_text.replace('ி'.encode("utf-8").decode("utf-8"), "p")
    input_text = input_text.replace('ீ'.encode("utf-8").decode("utf-8"), "P")

    return input_text