import Data.List
import Data.Char


isRepeatThing (c1 : c2 : rest) = [c1, c2] `isInfixOf` rest
isRepeatThing _ = False

isSandwichThing (c1 : _ : c2 : _) = c1 == c2
isSandwichThing _ = False

good s = hasRepeat && hasSandwich
  where hasRepeat = any isRepeatThing (tails s)
        hasSandwich = any isSandwichThing (tails s)

answer f = interact $ (++"\n") . show . f
main = answer $ length . filter good . lines
