# ANIMATE BALLS for MD codes (disks)

# usage example: "gnuplot -e 'nt=900; LX=10; LY=10' --persist animate2_ball.gnuplot"

set t wxt
#set t png

nt=1500
LX=20
LY=15

set xrange[0:LX]
set yrange[0:LY]
set size ratio LY/LX

cd 'data'

do for[count=0:nt]{
    pause 0.05
    frame = 'xy'.count
    if (count<1000) {frame='xy0'.count}
    if (count<100) {frame='xy00'.count}
    if (count<10) {frame='xy000'.count}
    archivo = frame.'.dat'
#    image = frame.'.png'
#    set o image
    plot archivo u 1:2:(1) w circles title archivo
}
