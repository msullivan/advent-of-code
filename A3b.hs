import Data.List
import Data.List.Extra

coord :: Char -> (Int, Int)
coord '^' = (0,  1)
coord 'v' = (0, -1)
coord '>' = ( 1, 0)
coord '<' = (-1, 0)
coord _ = (0, 0)

plusc (a, b) (c, d) = (a+c, b+d)

uninterleave [] = ([], [])
uninterleave [x] = ([x], [])
uninterleave (a : b : l) = (a : as, b : bs)
  where (as, bs) = uninterleave l

nus = scanl plusc (0, 0) . map coord
doit l = nus as ++ nus bs
  where (as, bs) = uninterleave l


answer f = interact $ (++"\n") . show . f
main = answer $ length . group . sort . doit
