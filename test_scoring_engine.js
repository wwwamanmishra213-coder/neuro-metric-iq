/**
 * NEURO-METRIC AUTOMATED TEST SUITE
 * -------------------------------------------------------------
 * Verifies mathematical correctness, statistical properties, edge cases,
 * boundary behaviors, and report consistency across all scoring modules.
 *
 * Execution: node test_scoring_engine.js
 */

const assert = require('assert');
const engine = require('./scoring-engine.js');

let totalTests = 0;
let passedTests = 0;
let failedTests = 0;

function runTest(testName, testFn) {
  totalTests++;
  try {
    testFn();
    passedTests++;
    console.log(`  ✓ [PASS] ${testName}`);
  } catch (err) {
    failedTests++;
    console.error(`  ✗ [FAIL] ${testName}`);
    console.error(`    Error: ${err.message}`);
  }
}

console.log('=============================================================');
console.log(`RUNNING NEUROMETRIC SCORING ENGINE AUDIT & VERIFICATION TESTS`);
console.log(`Engine Version: ${engine.ENGINE_VERSION}`);
console.log('=============================================================\n');

// -------------------------------------------------------------
// GROUP 1: MATHEMATICAL & STATISTICAL FOUNDATIONS
// -------------------------------------------------------------
console.log('GROUP 1: Mathematical & Statistical Foundations');

runTest('1. Zero correct answers produce 0.0% accuracy when at least one item was attempted', () => {
  const items = [
    { item_id: 1, user_choice: 2, is_correct: false },
    { item_id: 2, user_choice: 4, is_correct: false }
  ];
  const res = engine.scoreFluidReasoning(items);
  assert.strictEqual(res.items_attempted, 2);
  assert.strictEqual(res.items_correct, 0);
  assert.strictEqual(res.accuracy_pct, 0.0);
});

runTest('2. Perfect accuracy is exactly 100.0% when every attempted item is correct', () => {
  const items = [
    { item_id: 1, user_choice: 3, is_correct: true },
    { item_id: 2, user_choice: 1, is_correct: true },
    { item_id: 3, user_choice: 2, is_correct: true }
  ];
  const res = engine.scoreFluidReasoning(items);
  assert.strictEqual(res.items_attempted, 3);
  assert.strictEqual(res.items_correct, 3);
  assert.strictEqual(res.accuracy_pct, 100.0);
});

runTest('3. No attempted items produce null accuracy, NOT NaN or divide-by-zero error', () => {
  const items = [];
  const res = engine.scoreFluidReasoning(items);
  assert.strictEqual(res.items_attempted, 0);
  assert.strictEqual(res.items_correct, 0);
  assert.strictEqual(res.accuracy_pct, null);
  assert(!isNaN(res.items_correct));
});

runTest('4. Incorrect, omitted, and skipped items are counted appropriately', () => {
  const items = [
    { item_id: 1, user_choice: 2, is_correct: true },
    { item_id: 2, user_choice: null, is_correct: false }, // Omitted / skipped
    { item_id: 3, user_choice: 5, is_correct: false }
  ];
  const res = engine.scoreFluidReasoning(items);
  assert.strictEqual(res.items_attempted, 2); // 1 skipped
  assert.strictEqual(res.items_correct, 1);
  assert.strictEqual(res.accuracy_pct, 50.0);
});

runTest('5. Latency metrics use consistent seconds unit and calculate mean properly', () => {
  const items = [
    { item_id: 1, user_choice: 1, is_correct: true, latency_ms: 2000 },
    { item_id: 2, user_choice: 2, is_correct: true, latency_ms: 4000 }
  ];
  const res = engine.scoreFluidReasoning(items);
  assert.strictEqual(res.mean_latency_sec, 3.0);
});

runTest('6. Negative or invalid durations are rejected from latency statistics', () => {
  const items = [
    { item_id: 1, user_choice: 1, is_correct: true, latency_ms: -500 }, // Invalid negative
    { item_id: 2, user_choice: 2, is_correct: true, latency_ms: 2000 }
  ];
  const res = engine.scoreFluidReasoning(items);
  assert.strictEqual(res.mean_latency_sec, 2.0); // Only 2000ms included
});

// -------------------------------------------------------------
// GROUP 2: NORMAL DISTRIBUTION & PERCENTILES
// -------------------------------------------------------------
console.log('\nGROUP 2: Normal Distribution & Percentile Properties');

runTest('7. Percentile calculations are strictly monotonic across standard scores', () => {
  const scores = [70, 85, 100, 112, 115, 123, 130, 145];
  let prevPercentile = -1;
  scores.forEach(s => {
    const p = engine.calculateTheoreticalPercentile(s);
    assert(p > prevPercentile, `Expected ${p} > ${prevPercentile} for score ${s}`);
    prevPercentile = p;
  });
});

runTest('8. Reference mean (100) maps to exactly 50.0th percentile under N(100, 15)', () => {
  const p = engine.calculateTheoreticalPercentile(100, 100, 15);
  assert(Math.abs(p - 50.0) < 0.01, `Expected 50.0, got ${p}`);
});

runTest('9. High-ceiling cutoff (130) maps to approximately 97.7th percentile', () => {
  // z = (130 - 100) / 15 = 2.000. True Phi(2) = 0.9772499 => 97.7%
  const p = engine.calculateTheoreticalPercentile(130, 100, 15);
  assert(Math.abs(p - 97.7) < 0.1, `Expected ~97.7, got ${p}`);
});

runTest('10. User audit score (112) maps to approximately 78.8th percentile', () => {
  // z = (112 - 100) / 15 = 0.800. True Phi(0.8) = 0.78814 => 78.8%
  const p = engine.calculateTheoreticalPercentile(112, 100, 15);
  assert(Math.abs(p - 78.8) < 0.1, `Expected ~78.8, got ${p}`);
});

// -------------------------------------------------------------
// GROUP 3: UNCERTAINTY & CONFIDENCE INTERVALS
// -------------------------------------------------------------
console.log('\nGROUP 3: Uncertainty & Confidence Intervals');

runTest('11. Confidence intervals are strictly reproducible from score and SEM (1.96 * SEM)', () => {
  // For score = 112, SEM = 3.67: margin = round(1.95996 * 3.67) = round(7.19) = 7
  const ci = engine.calculateConfidenceInterval(112, 3.67, 0.95);
  assert.strictEqual(ci.margin, 7);
  assert.strictEqual(ci.lower, 105);
  assert.strictEqual(ci.upper, 119);
  assert.strictEqual(ci.confidence_level, "95%");
  assert.strictEqual(ci.status, "THEORETICAL_ESTIMATE");
});

runTest('12. Missing score produces unavailable confidence interval structure without crashing', () => {
  const ci = engine.calculateConfidenceInterval(null);
  assert.strictEqual(ci.lower, null);
  assert.strictEqual(ci.upper, null);
  assert.strictEqual(ci.status, "UNAVAILABLE");
});

// -------------------------------------------------------------
// GROUP 4: INTEGRATION, COMPOSITE, AND CLINICAL DISCREPANCY
// -------------------------------------------------------------
console.log('\nGROUP 4: Subtests, Composite & Clinical Discrepancy (GAI)');

runTest('13. User audit case reproduces exact factor scores (Gf=123, Gwm=114, Gq=109, Gs=78)', () => {
  // Gf: 7 of 8 correct
  const gfItems = Array.from({ length: 8 }, (_, i) => ({
    item_id: i + 1,
    user_choice: 1,
    is_correct: i < 7,
    latency_ms: 2200
  }));
  const gfRes = engine.scoreFluidReasoning(gfItems);
  assert.strictEqual(gfRes.items_correct, 7);
  assert.strictEqual(gfRes.heuristic_index, 123);

  // Gwm: span 6, 3 successes
  const gwmRes = engine.scoreWorkingMemory([], 6, 3);
  assert.strictEqual(gwmRes.heuristic_index, 114);

  // Gq: 4 of 6 correct
  const gqItems = Array.from({ length: 6 }, (_, i) => ({
    item_id: i + 1,
    user_choice: 1,
    is_correct: i < 4,
    latency_ms: 3100
  }));
  const gqRes = engine.scoreQuantitative(gqItems);
  assert.strictEqual(gqRes.items_correct, 4);
  assert.strictEqual(gqRes.heuristic_index, 109);

  // Gs: 7 correct, 2 incorrect in 45s => net = 7 - 1 = 6.0 => z = (6 - 12)/4 = -1.5 => 78
  const gsRes = engine.scoreProcessingSpeed([], { correct: 7, incorrect: 2, durationSec: 45 });
  assert.strictEqual(gsRes.heuristic_index, 78);
});

runTest('14. Composite report reproduces FSIQ=112 and detects 45-point discrepancy triggering GAI in 120-121 range', () => {
  const gf = engine.scoreFluidReasoning(Array.from({ length: 8 }, (_, i) => ({ item_id: i+1, user_choice: 1, is_correct: i < 7 })));
  const gwm = engine.scoreWorkingMemory([], 6, 3);
  const gq = engine.scoreQuantitative(Array.from({ length: 6 }, (_, i) => ({ item_id: i+1, user_choice: 1, is_correct: i < 4 })));
  const gs = engine.scoreProcessingSpeed([], { correct: 7, incorrect: 2, durationSec: 45 });

  const report = engine.generateAssessmentReport({ Gf: gf, Gwm: gwm, Gq: gq, Gs: gs });

  assert.strictEqual(report.composite.value, 112);
  assert.strictEqual(report.composite.theoretical_percentile, 78.8);
  assert.strictEqual(report.status, "COMPLETED");

  // Clinical Discrepancy & GAI check
  assert.strictEqual(report.discrepancy_analysis.detected, true);
  assert.strictEqual(report.discrepancy_analysis.speed_discrepancy_points, 45);
  // GAI exact calculation: 100 + 15 * ((0.6 * 1.5556 + 0.4 * 0.6) / 0.85) = 120.71 => 121
  assert.strictEqual(report.discrepancy_analysis.gai_index, 121);
  assert(report.discrepancy_analysis.gai_theoretical_percentile >= 91.0);

  // 95% CI Check: [105, 119]
  assert.strictEqual(report.uncertainty.confidence_interval[0], 105);
  assert.strictEqual(report.uncertainty.confidence_interval[1], 119);
});

runTest('15. Balanced profile does not trigger GAI alert and maintains unitary composite status', () => {
  // All subtests near 100
  const gf = engine.scoreFluidReasoning(Array.from({ length: 8 }, (_, i) => ({ item_id: i+1, user_choice: 1, is_correct: i < 4 }))); // z = -0.11 => 98
  const gwm = engine.scoreWorkingMemory([], 5, 2); // z = -0.08 => 99
  const gq = engine.scoreQuantitative(Array.from({ length: 6 }, (_, i) => ({ item_id: i+1, user_choice: 1, is_correct: i < 3 }))); // z = -0.07 => 99
  const gs = engine.scoreProcessingSpeed([], { correct: 12, incorrect: 0, durationSec: 45 }); // z = 0 => 100

  const report = engine.generateAssessmentReport({ Gf: gf, Gwm: gwm, Gq: gq, Gs: gs });
  assert.strictEqual(report.discrepancy_analysis.detected, false);
  assert.strictEqual(report.discrepancy_analysis.gai_index, null);
});

runTest('16. Incomplete assessment is flagged as INCOMPLETE and metadata acknowledges missing norms', () => {
  const gf = engine.scoreFluidReasoning(Array.from({ length: 8 }, (_, i) => ({ item_id: i+1, user_choice: 1, is_correct: i < 4 })));
  
  // Only 1 subtest supplied
  const report = engine.generateAssessmentReport({ Gf: gf, Gwm: null, Gq: null, Gs: null });
  assert.strictEqual(report.status, "INCOMPLETE");
  assert.strictEqual(report.norm_reference.validation_status, "NO_CLINICAL_NORMS_ATTACHED");
  assert.strictEqual(report.norm_reference.sample_size, null);
});

console.log('\n=============================================================');
console.log(`TEST SUMMARY: ${passedTests} PASSED, ${failedTests} FAILED (TOTAL: ${totalTests})`);
console.log('=============================================================');

if (failedTests > 0) {
  process.exit(1);
} else {
  process.exit(0);
}
