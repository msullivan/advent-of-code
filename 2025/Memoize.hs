-- automatic function memoization using laziness
-- essentially builds implicit lazy (potentially infinite) search trees
-- inspired by https://hackage.haskell.org/package/memoize-1.1.2/docs/Data-Function-Memoize.html
-- but simplified for educational purposes.

-- Interestingly, in the one test I've done, memoizing a recursive
-- function that takes (Int, Int), this was actually about 10% faster
-- than the memoize package.  Possibly their more complex explicit-tree based
-- implementation for Int isn't actually better than the dumb thing I do!

module Memoize where

import Data.List (uncons)
import Data.Bool (bool)

class Memoize a where
  memoize :: (a -> v) -> a -> v

memoFix :: Memoize a => ((a -> v) -> a -> v) -> a -> v
memoFix ff = f
  where f = memoize (ff f)

-- Core memoization primitives for unit, product, and sums.

-- All of my other implementations work by coercing values into these
-- types and back.

instance Memoize () where
  -- We memoize () by binding its unique result to a variable, and
  -- then reusing that
  memoize f = mf
    where v = f ()
          mf () = v

instance (Memoize a, Memoize b) => Memoize (a, b) where
  memoize f = mf
    -- We memoize a product by memoizing the elements individually
    where fc = memoize $ \xa -> memoize $ \xb -> f (xa, xb)
          mf (xa, xb) = fc xa xb

instance (Memoize a, Memoize b) => Memoize (Either a b) where
  memoize f = mf
    -- We memoize a sum by memoizing the left and right cases in
    -- saved variables, and then dispatching to the appropriate one.
    where fl = memoize $ \x -> f (Left x)
          fr = memoize $ \x -> f (Right x)

          mf (Left x) = fl x
          mf (Right x) = fr x

----

instance Memoize Bool where
  -- Bool <=> Either () ()
  memoize f = memoize (f . eitherToBool) . boolToEither
    where
      boolToEither = bool (Left ()) (Right ())
      eitherToBool = either (const False) (const True)

instance (Memoize a) => Memoize (Maybe a) where
  -- Maybe a <=> Either () a
  memoize f = memoize (f . eitherToMaybe) . maybeToEither
    where
      maybeToEither = maybe (Left ()) Right
      eitherToMaybe = either (const Nothing) Just

instance (Memoize a) => Memoize [a] where
  -- [a] <=> Maybe (a, [a])
  memoize f = memoize (f . maybeToList) . listToMaybe
    where
      listToMaybe = uncons
      maybeToList = maybe [] (uncurry (:))

-- Numbers

-- Integer <=> (Bool, [Bool])
-- Where the first bool represents the sign bit and the list has all
-- the other bits

-- (well it's actually not quite a bijection because we could have -0
-- or extra leading 0s, but we won't in practice)

integerToList :: Integer -> (Bool, [Bool])
integerToList n = (n < 0, posToList (abs n))
  where
    posToList 0 = []
    posToList n = (n `mod` 2 == 1) : posToList (n `div` 2)

listToInteger :: (Bool, [Bool]) -> Integer
listToInteger (neg, l) = (if neg then -1 else 1) * listToPos l
  where
    listToPos [] = 0
    listToPos (x:xs) = (if x then 1 else 0) + 2 * listToPos xs


instance Memoize Integer where
  memoize f = memoize (f . listToInteger) . integerToList

instance Memoize Int where
  memoize f = memoize (f . fromInteger) . toInteger

instance Memoize Word where
  memoize f = memoize (f . fromInteger) . toInteger

instance Memoize Char where
  memoize f = memoize (f . toEnum) . fromEnum

-- It would be easy to add Word and all the different Words and stuff
