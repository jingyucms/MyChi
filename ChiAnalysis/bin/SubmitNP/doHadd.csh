#!/bin/tcsh

#foreach n (2500 3000 3500 4000 4500 5000 6000)
foreach n (3500)
    hadd Axial_Dijet_LO_Mphi_${n}_1_1p0_1p0_Smeared.root `xrdfsls -u /store/user/jingyu/events/dmaxial_CrystalBall/ | grep "m${n}"`
end
