import Control.Monad
import Data.List.Extra
import Data.Maybe
--import Data.Function.Memoize
--import Memoize
import Data.Function
import qualified Data.Char
import qualified Data.Map as Map
import Debug.Trace

{-
data Spell = Spell
     { Name :: String
     , Cost :: Int
     , Damage :: Int
     , Heal :: Int
     , Armor :: Int
     , Recharge :: Int
     , Duration :: Int
     }
-}

spells = [
  ("Magic Missile", 53, 1),
  ("Drain", 73, 1),
  ("Shield", 113, 6),
  ("Poison", 173, 6),
  ("Recharge", 229, 5)
  ]

plus (a1, a2, a3) (b1, b2, b3) = (a1+b1, a2+b2, a3+b3)
zero = (0,0,0)

apply (_, _, 0) st = st -- asdf
apply (spell, _, _) st@(a, mhp, bhp, mana, s) = e spell
  where e "Magic Missile" = (a, mhp, bhp-4, mana, s)
        e "Drain" = (a, mhp+2, bhp-2, mana, s)
        e "Shield" = st
        e "Poison" = (a, mhp, bhp-3, mana, s)
        e "Recharge" = (a, mhp, bhp, mana+101, s)

name (n, _, _) = n
cost (_, c, _) = c
won (_, _, b, _, _) = b <= 0

hasShield = any ((=="Shield") . name)

bossHP = 51
bossDmg = 9


theirTurn s@(active, myhp, bosshp, mana, spent) l =
  let s'@(_, myhp', bosshp', mana', _) = foldr apply s active
      active' = filter (\(_,_,t) -> t > 0) $
                map (\(a,b,c) -> (a,b,c-1)) active
  in if won s' then return (spent, l) else
       let armor = if hasShield active' then 7 else 0
           dmg = max 1 $ bossDmg - armor
           myhp'' = myhp' - dmg
       in if myhp'' <= 0 then [] else
            myTurn (active', myhp'', bosshp', mana', spent) l

myTurn s@(active, myhp, bosshp, mana, spent) l =
  let s'@(_, myhp', bosshp', mana', _) = foldr apply s active
      active' = filter (\(_,_,t) -> t > 0) $
                map (\(a,b,c) -> (a,b,c-1)) active
  in if won s' then return (spent, l) else
       do spell <- spells
          guard $ not $ any (\s -> name s == name spell) active'
          let mana'' = mana' - (cost spell)
          let spent' = spent + cost spell
          guard $ mana'' >= 0
           -- HACK, optimiz ; doing this sort of pruning properly in
           -- haskell is actually kind of annoying
          guard $ spent' < 1000
          theirTurn (spell:active', myhp', bosshp', mana'', spent') (name spell : l)

answer = minimum $ myTurn ([], 50, bossHP, 500, 0) []
main = putStrLn $ show answer
