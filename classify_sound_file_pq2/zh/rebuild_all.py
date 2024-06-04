import os,sys

workplaceRoot =r'D:\code\git\Persona-Modding\classify_sound_file_pq2\zh'
os.chdir(workplaceRoot)

# rebuild charset first
# import build_fake_charset.build_charset as bfcbc
# bfcbc.buildCharset()

# import build_fake_charset.build_new_charset_bmp as bfcbc
# bfcbc.buildCharsetBmp()

# import build_fake_charset.build_new_charset_bcfnt as bfcbc
# bfcbc.buildCharsetBcFnt()




import facility.pack.top_arc.bf as fptb
fptb.rebuildBf()

import facility.pack.top_arc.bmd as fptb
fptb.rebuildAllBmd()

import facility.pack.top_arc.arc as fpta
fpta.repack()

import dungeon.pack.dng_com_arc.bmd as dpdb
dpdb.rebuildAllBmd()

import dungeon.pack.dng_com_arc.bf as dpdb
dpdb.rebuildBf()

import dungeon.pack.dng_com_arc.arc as dpda
dpda.repack()

import dungeon.message.bmd as dmb
dmb.rebuildAllBmd()

import dungeon.message.objective.free.bmd as dmofb
dmofb.rebuildAllBmd()

import dungeon.message.objective.quest.bmd as dmofq
dmofq.rebuildAllBmd()

import attraction.tbl as at
at.rebuildTbl()

import dungeon.script.charaTalk.bf as dscb
dscb.rebuildBf()

import dungeon.script.support.bf as dssb
dssb.rebuildBf()

# import battle.support.bvp_bmd as bsb
# bsb.rebuilBvp()

# import battle.result.bf as brb
# brb.rebuildBf()

import camp.bf as cb
cb.rebuildBf()

import camp.dictionary_tbl as cd
cd.rebuildTbl()

import camp.skladd_arc.arc as cka
cka.rebuilArc()

import camp.skladdex_arc.arc as cka
cka.rebuilArc()

import battle.result.bmd as brb
brb.rebuildAllBmd()

import battle.result.persona_get_bin.bmd as brpb
brpb.rebuildBin()

import battle.event.rebuild_msg as ber
ber.rebuildBMDs()

import battle.pack.btl_com_arc.bmd as bbab
bbab.rebuildAllBmd()

import battle.pack.btl_com_arc.mbm as bbam
bbam.rebuildAllMbm()

import battle.pack.btl_com_arc.arc as bpba
bpba.repack()

import battle.message.rebuild_bmd as bmr
bmr.rebuildBMDs()

import battle.message.rebuild_mbm as bmr
bmr.rebuildMbm()

import battle.message.rebuild_tbl as bmr
bmr.rebuilTbl()

import battle.support.message.rebuild_bmd as bsm
bsm.rebuildBMDs()

import battle.table.rebuild_tbl as bt
bt.rebuildTbl()

import facility.rebuild_bmd as fr
fr.rebuildBMDs()

import facility.bf_rebuild as fb
fb.rebuilBf()

import facility.bf_fail_rebuild as fb
fb.rebuilBf()

import facility.pack.cmbroot_arc.bf as fpc
fpc.rebuildBf()

#shitty global
import facility.pack.cmbroot_arc.bmd as fpc
fpc.rebuildAllBmd()

# rebuild arc at the end
import facility.pack.cmbroot_arc.arc as fpca
fpca.repack()


import facility.pack.shop_arc.bf as fpsb
fpsb.rebuildBf()


import facility.pack.shop_arc.bmd as fpsb
fpsb.rebuildAllBmd()

import facility.pack.shop_arc.arc as fpsa
fpsa.rebuilArc()

import init.tutorialtable_bin.ftd as itf
itf.rebuildFtd()

import init.tutorialtable_bin.bin as tb
tb.repack()

import init.spkrtbl_bin.spkrtbl as iss
iss.rebuilBin()

import init.cmptable_bin.rebuild_bmd as icbr
icbr.rebuildBMDs()

import init.cmptable_bin.rebuild_ctd as icbr
icbr.rebuildCtd()

import init.cmptable_bin.repack_bin as icbr
icbr.buildBin()

import init.fcltable_bin.rebuild_ftd as ifr
ifr.rebuildFtd()

import init.fcltable_bin.repack_bin as ifr
ifr.rebuildBin()

# shitty os.chdir in it
import init.itemtbl_bin.itemtbl as iii
iii.rebuild()
os.chdir(workplaceRoot)

import init.rebuild_bmd as ir
ir.rebuildBMDs()

import item.rebuild_mbm as ir
ir.rebuildMbm()

import item.rebuild_tbl as ir
ir.rebuildTbl()

import tutorial.scr.rebuild_msg as tsr
tsr.rebuildBMDs()

# import event.rebuild_msg as er
# er.rebuildEventMsg()

sys.path.append(r"D:\code\git\Persona-Modding\classify_sound_file_pq2\3dstool")
import rebuild_cpk as rc
rc.rebuildCPK()