import Control.Monad
import Data.List.Extra
import Data.Maybe
--import Data.Function.Memoize
--import Memoize
import Data.Function
import qualified Data.Char
import qualified Data.Map as Map
import Debug.Trace

weapons = [
  (8,4,0),
  (10,5,0),
  (25,6,0),
  (40,7,0),
  (74,8,0)
  ]
armor = [
  (13,0,1),
  (31,0,2),
  (53,0,3),
  (75,0,4),
  (102,0,5)
  ]
rings = [
  (25,1,0),
  (50,2,0),
  (100,3,0),
  (20,0,1),
  (40,0,2),
  (80,0,3)
  ]

plus (a1, a2, a3) (b1, b2, b3) = (a1+b1, a2+b2, a3+b3)
zero = (0,0,0)

loadouts = do
  weapon <- weapons
  armor <- filter ((<=1) . length) $ subsequences armor
  rings <- filter ((<=2) . length) $ subsequences rings
  let gear = [weapon] ++ armor ++ rings
  return $ foldr plus zero gear

myHP = 100
bossHP = 104
bossDmg = 8
bossArmor = 1

fight a@(a_hp, a_dmg, a_arm) (b_hp, b_dmg, b_arm) =
  let dmg = max 1 $ a_dmg-b_arm
      b_hp' = b_hp - dmg
  in if b_hp' <= 0 then True else
       not $ fight (b_hp', b_dmg, b_arm) a

tryLoadout (_, dmg, arm) = fight (myHP, dmg, arm) (bossHP, bossDmg, bossArmor)

answer = minimum $ map (\(a,_,_)->a) $ filter tryLoadout loadouts
main = putStrLn $ show answer
