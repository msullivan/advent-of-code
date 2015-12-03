import Data.List
import Data.List.Extra

type Box = (Int, Int, Int)

readBox :: String -> Box
readBox s =
  let [a, b, c] = map read $ wordsBy (=='x') s
  in (a, b, c)

calcBox :: Box -> Int
calcBox (l, w, h) =
  let sides = sort [l*w, l*h, w*h]
  in 2*sum sides + head sides

main = interact $ (++"\n") . show . sum . map (calcBox . readBox) . lines
