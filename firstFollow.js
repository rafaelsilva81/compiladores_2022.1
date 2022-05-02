// Special "empty" symbol.
var EPSILON = "ε";

var firstSets = {};
var followSets = {};

/**
 * Rules for First Sets
 *
 * - If X is a terminal then First(X) is just X!
 * - If there is a Production X → ε then add ε to first(X)
 * - If there is a Production X → Y1Y2..Yk then add first(Y1Y2..Yk) to first(X)
 * - First(Y1Y2..Yk) is either
 *     - First(Y1) (if First(Y1) doesn't contain ε)
 *     - OR (if First(Y1) does contain ε) then First (Y1Y2..Yk) is everything
 *       in First(Y1) <except for ε > as well as everything in First(Y2..Yk)
 *     - If First(Y1) First(Y2)..First(Yk) all contain ε then add ε
 *       to First(Y1Y2..Yk) as well.
 */

function buildFirstSets(grammar) {
  firstSets = {};
  buildSet(firstOf);
}

function firstOf(symbol) {

  // A set may already be built from some previous analysis
  // of a RHS, so check whether it's already there and don't rebuild.
  if (firstSets[symbol]) {
    return firstSets[symbol];
  }

  // Else init and calculate.
  var first = firstSets[symbol] = {};

  // If it's a terminal, its first set is just itself.
  if (isTerminal(symbol)) {
    first[symbol] = true;
    return firstSets[symbol];
  }

  var productionsForSymbol = getProductionsForSymbol(symbol);
  for (var k in productionsForSymbol) {
    var production = getRHS(productionsForSymbol[k]);

    for (var i = 0; i < production.length; i++) {
      var productionSymbol = production[i];

      // Epsilon goes to the first set.
      if (productionSymbol === EPSILON) {
        first[EPSILON] = true;
        break;
      }

      // Else, the first is a non-terminal,
      // then first of it goes to first of our symbol
      // (unless it's an epsilon).
      var firstOfNonTerminal = firstOf(productionSymbol);

      // If first non-terminal of the RHS production doesn't
      // contain epsilon, then just merge its set with ours.
      if (!firstOfNonTerminal[EPSILON]) {
        merge(first, firstOfNonTerminal);
        break;
      }

      // Else (we got epsilon in the first non-terminal),
      //
      //   - merge all except for epsilon
      //   - eliminate this non-terminal and advance to the next symbol
      //     (i.e. don't break this loop)
      merge(first, firstOfNonTerminal, [EPSILON]);
      // don't break, go to the next `productionSymbol`.
    }
  }

  return first;
}

/**
 * We have the following data structure for our grammars:
 *
 * var grammar = {
 *   1: 'S -> F',
 *   2: 'S -> (S + F)',
 *   3: 'F -> a',
 * };
 *
 * Given symbol `S`, the function returns `S -> F`,
 * and `S -> (S + F)` productions.
 */
function getProductionsForSymbol(symbol) {
  var productionsForSymbol = {};
  for (var k in grammar) {
    if (grammar[k][0] === symbol) {
      productionsForSymbol[k] = grammar[k];
    }
  }
  return productionsForSymbol;
}

/**
 * Given production `S -> F`, returns `S`.
 */
function getLHS(production) {
  return production.split('->')[0].replace(/\s+/g, '');
}

/**
 * Given production `S -> F`, returns `F`.
 */
function getRHS(production) {
  return production.split('->')[1].replace(/\s+/g, '');
}

/**
 * Rules for Follow Sets
 *
 * - First put $ (the end of input marker) in Follow(S) (S is the start symbol)
 * - If there is a production A → aBb, (where a can be a whole string)
 *   then everything in FIRST(b) except for ε is placed in FOLLOW(B).
 * - If there is a production A → aB, then everything in
 *   FOLLOW(A) is in FOLLOW(B)
 * - If there is a production A → aBb, where FIRST(b) contains ε,
 *   then everything in FOLLOW(A) is in FOLLOW(B)
 */

function buildFollowSets(grammar) {
  followSets = {};
  buildSet(followOf);
}

function followOf(symbol) {

  // If was already calculated from some previous run.
  if (followSets[symbol]) {
    return followSets[symbol];
  }

  // Else init and calculate.
  var follow = followSets[symbol] = {};

  // Start symbol always contain `$` in its follow set.
  if (symbol === START_SYMBOL) {
    follow['$'] = true;
  }

  // We need to analyze all productions where our
  // symbol is used (i.e. where it appears on RHS).
  var productionsWithSymbol = getProductionsWithSymbol(symbol);
  for (var k in productionsWithSymbol) {
    var production = productionsWithSymbol[k];
    var RHS = getRHS(production);

    // Get the follow symbol of our symbol.
    var symbolIndex = RHS.indexOf(symbol);
    var followIndex = symbolIndex + 1;

    // We need to get the following symbol, which can be `$` or
    // may contain epsilon in its first set. If it contains epsilon, then
    // we should take the next following symbol: `A -> aBCD`: if `C` (the
    // follow of `B`) can be epsilon, we should consider first of `D` as well
    // as the follow of `B`.

    while (true) {

      if (followIndex === RHS.length) { // "$"
        var LHS = getLHS(production);
        if (LHS !== symbol) { // To avoid cases like: B -> aB
          merge(follow, followOf(LHS));
        }
        break;
      }

      var followSymbol = RHS[followIndex];

      // Follow of our symbol is anything in the first of the following symbol:
      // followOf(symbol) is firstOf(followSymbol), except for epsilon.
      var firstOfFollow = firstOf(followSymbol);

      // If there is no epsilon, just merge.
      if (!firstOfFollow[EPSILON]) {
        merge(follow, firstOfFollow);
        break;
      }

      merge(follow, firstOfFollow, [EPSILON]);
      followIndex++;
    }
  }

  return follow;
}

function buildSet(builder) {
  for (var k in grammar) {
    builder(grammar[k][0]);
  }
}

/**
 * Finds productions where a non-terminal is used. E.g., for the
 * symbol `S` it finds production `(S + F)`, and for the symbol `F`
 * it finds productions `F` and `(S + F)`.
 */
function getProductionsWithSymbol(symbol) {
  var productionsWithSymbol = {};
  for (var k in grammar) {
    var production = grammar[k];
    var RHS = getRHS(production);
    if (RHS.indexOf(symbol) !== -1) {
      productionsWithSymbol[k] = production;
    }
  }
  return productionsWithSymbol;
}

function isTerminal(symbol) {
  return !/[A-Z]/.test(symbol);
}

function merge(to, from, exclude) {
  exclude || (exclude = []);
  for (var k in from) {
    if (exclude.indexOf(k) === -1) {
      to[k] = from[k];
    }
  }
}

function printGrammar(grammar) {
  console.log('Grammar:\n');
  for (var k in grammar) {
    console.log('  ', grammar[k]);
  }
  console.log('');
}

function printSet(name, set) {
  console.log(name + ': \n');
  for (var k in set) {
    console.log('  ', k, ':', Object.keys(set[k]));
  }
  console.log('');
}

// Testing

// --------------------------------------------------------------------------
// Example 1 of a simple grammar, generates: a, or (a + a), etc.
// --------------------------------------------------------------------------

var grammar = {
  1: 'S -> F',
  2: 'S -> (S + F)',
  3: 'F -> a',
};

var START_SYMBOL = 'S';

printGrammar(grammar);

buildFirstSets(grammar);
printSet('First sets', firstSets);

buildFollowSets(grammar);
printSet('Follow sets', followSets);
