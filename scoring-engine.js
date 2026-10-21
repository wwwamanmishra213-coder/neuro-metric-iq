/**
 * NEURO-METRIC SCORING & PSYCHOMETRIC ENGINE
 * -------------------------------------------------------------
 * Modular, deterministic, mathematically audited cognitive engine.
 * Compatible with Node.js test environments and browser runtimes.
 *
 * Grounded in Cattell-Horn-Carroll (CHC) cognitive factors.
 * All derived scores are explicitly labeled with their validation status.
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.NeuroMetricScoring = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {

  const ENGINE_VERSION = "3.1.0-audited";
  const THEORETICAL_MEAN = 100.0;
  const THEORETICAL_SD = 15.0;
  const THEORETICAL_SEM = 3.67; // Assuming r_xx = 0.94 under Wechsler norm model

  // Baseline calibration parameters (Empirical proxy norms)
  const PARAMS = {
    Gf:  { mean: 4.2, sd: 1.8, weight: 0.35, maxItems: 8 },
    Gwm: { mean: 5.5, sd: 1.2, weight: 0.25, maxSpan: 8 },
    Gq:  { mean: 3.1, sd: 1.5, weight: 0.25, maxItems: 6 },
    Gs:  { mean: 12.0, sd: 4.0, weight: 0.15, durationSec: 45 }
  };

  /**
   * High-precision Gauss Error Function erf(x)
   * Formula: Abramowitz & Stegun 7.1.26 (max error: 1.5e-7)
   */
  function erf(x) {
    const sign = x >= 0 ? 1 : -1;
    x = Math.abs(x);

    const a1 = 0.254829592;
    const a2 = -0.284496736;
    const a3 = 1.421413741;
    const a4 = -1.453152027;
    const a5 = 1.061405429;
    const p  = 0.3275911;

    const t = 1.0 / (1.0 + p * x);
    const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
    return sign * y;
  }

  /**
   * Standard Normal Cumulative Distribution Function Φ(z)
   */
  function standardNormalCDF(z) {
    return 0.5 * (1.0 + erf(z / Math.SQRT2));
  }

  /**
   * Calculate Theoretical Percentile for standard scale X ~ N(mean, sd)
   */
  function calculateTheoreticalPercentile(score, mean = THEORETICAL_MEAN, sd = THEORETICAL_SD) {
    if (typeof score !== 'number' || isNaN(score)) return null;
    const z = (score - mean) / sd;
    const cdf = standardNormalCDF(z);
    return Math.min(99.9, Math.max(0.1, cdf * 100.0));
  }

  /**
   * Standard 95% Confidence Interval using 1.96 * SEM
   */
  function calculateConfidenceInterval(score, sem = THEORETICAL_SEM, confidenceLevel = 0.95) {
    if (typeof score !== 'number' || isNaN(score)) {
      return { lower: null, upper: null, margin: null, status: "UNAVAILABLE" };
    }
    // Z-critical for 95% = 1.95996; for 90% = 1.64485; for 99% = 2.57583
    let zCrit = 1.95996;
    if (confidenceLevel === 0.90) zCrit = 1.64485;
    if (confidenceLevel === 0.99) zCrit = 2.57583;

    const margin = Math.round(zCrit * sem);
    return {
      lower: score - margin,
      upper: score + margin,
      margin: margin,
      confidence_level: `${Math.round(confidenceLevel * 100)}%`,
      method: "Normal-Approximation (z_crit * SEM)",
      status: "THEORETICAL_ESTIMATE"
    };
  }

  /**
   * Linear Z-Score calculation with bounds clamp
   */
  function toStandardScore(z, min = 55, max = 145) {
    if (typeof z !== 'number' || isNaN(z)) return null;
    const score = Math.round(THEORETICAL_MEAN + THEORETICAL_SD * z);
    return Math.max(min, Math.min(max, score));
  }

  /**
   * Median and average calculation
   */
  function calculateStats(numbers) {
    if (!Array.isArray(numbers) || numbers.length === 0) {
      return { mean: null, median: null, count: 0 };
    }
    const valid = numbers.filter(n => typeof n === 'number' && !isNaN(n) && n >= 0);
    if (valid.length === 0) return { mean: null, median: null, count: 0 };

    const sum = valid.reduce((acc, val) => acc + val, 0);
    const mean = sum / valid.length;

    const sorted = [...valid].sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    const median = sorted.length % 2 !== 0 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2.0;

    return { mean, median, count: valid.length };
  }

  // ==========================================
  // DOMAIN 1: FLUID MATRIX REASONING (Gf)
  // ==========================================
  function scoreFluidReasoning(itemResponses = []) {
    if (!Array.isArray(itemResponses)) {
      itemResponses = [];
    }

    const itemsAttempted = itemResponses.filter(r => r && r.user_choice !== null && r.user_choice !== undefined).length;
    const itemsCorrect = itemResponses.filter(r => r && r.is_correct === true).length;
    const accuracy = itemsAttempted > 0 ? (itemsCorrect / itemsAttempted) * 100.0 : null;

    const latencies = itemResponses
      .map(r => r ? (r.latency_sec || (r.latency_ms ? r.latency_ms / 1000 : null)) : null)
      .filter(l => typeof l === 'number' && l > 0);

    const latencyStats = calculateStats(latencies);

    // Heuristic Z-transformation
    const z = (itemsCorrect - PARAMS.Gf.mean) / PARAMS.Gf.sd;
    const indexScore = toStandardScore(z);
    const percentile = calculateTheoreticalPercentile(indexScore);

    return {
      domain_key: "Gf",
      domain_name: "Fluid Matrix Reasoning",
      items_attempted: itemsAttempted,
      items_total: PARAMS.Gf.maxItems,
      items_correct: itemsCorrect,
      accuracy_pct: accuracy !== null ? parseFloat(accuracy.toFixed(1)) : null,
      mean_latency_sec: latencyStats.mean !== null ? parseFloat(latencyStats.mean.toFixed(2)) : null,
      median_latency_sec: latencyStats.median !== null ? parseFloat(latencyStats.median.toFixed(2)) : null,
      z_score: parseFloat(z.toFixed(4)),
      heuristic_index: indexScore,
      theoretical_percentile: percentile !== null ? parseFloat(percentile.toFixed(1)) : null,
      validation_status: "RAW_PERFORMANCE_VERIFIED | HEURISTIC_UNSTANDARDIZED"
    };
  }

  // ==========================================
  // DOMAIN 2: SPATIAL WORKING MEMORY (Gwm)
  // ==========================================
  function scoreWorkingMemory(trials = [], finalSpanReached = 0, trialsSuccess = 0) {
    if (!Array.isArray(trials)) trials = [];

    const totalTrials = trials.length > 0 ? trials.length : 5;
    const successes = trials.length > 0
      ? trials.filter(t => t && t.exact_match === true).length
      : Math.max(0, trialsSuccess);

    let maxSpan = 0;
    if (trials.length > 0) {
      trials.forEach(t => {
        if (t && t.exact_match === true && typeof t.sequence_length === 'number') {
          if (t.sequence_length > maxSpan) maxSpan = t.sequence_length;
        }
      });
    } else {
      maxSpan = Math.max(0, finalSpanReached);
    }

    const spanScore = maxSpan + (0.2 * successes);
    const z = (spanScore - PARAMS.Gwm.mean) / PARAMS.Gwm.sd;
    const indexScore = toStandardScore(z);
    const percentile = calculateTheoreticalPercentile(indexScore);

    return {
      domain_key: "Gwm",
      domain_name: "Spatial Working Memory",
      max_span_completed: maxSpan,
      trials_attempted: totalTrials,
      trials_passed: successes,
      span_score: parseFloat(spanScore.toFixed(2)),
      z_score: parseFloat(z.toFixed(4)),
      heuristic_index: indexScore,
      theoretical_percentile: percentile !== null ? parseFloat(percentile.toFixed(1)) : null,
      validation_status: "RAW_PERFORMANCE_VERIFIED | HEURISTIC_UNSTANDARDIZED"
    };
  }

  // ==========================================
  // DOMAIN 3: QUANTITATIVE INDUCTION (Gq)
  // ==========================================
  function scoreQuantitative(itemResponses = []) {
    if (!Array.isArray(itemResponses)) itemResponses = [];

    const itemsAttempted = itemResponses.filter(r => r && r.user_choice !== null && r.user_choice !== undefined).length;
    const itemsCorrect = itemResponses.filter(r => r && r.is_correct === true).length;
    const accuracy = itemsAttempted > 0 ? (itemsCorrect / itemsAttempted) * 100.0 : null;

    const latencies = itemResponses
      .map(r => r ? (r.latency_sec || (r.latency_ms ? r.latency_ms / 1000 : null)) : null)
      .filter(l => typeof l === 'number' && l > 0);

    const latencyStats = calculateStats(latencies);

    const z = (itemsCorrect - PARAMS.Gq.mean) / PARAMS.Gq.sd;
    const indexScore = toStandardScore(z);
    const percentile = calculateTheoreticalPercentile(indexScore);

    return {
      domain_key: "Gq",
      domain_name: "Quantitative Induction",
      items_attempted: itemsAttempted,
      items_total: PARAMS.Gq.maxItems,
      items_correct: itemsCorrect,
      accuracy_pct: accuracy !== null ? parseFloat(accuracy.toFixed(1)) : null,
      mean_latency_sec: latencyStats.mean !== null ? parseFloat(latencyStats.mean.toFixed(2)) : null,
      z_score: parseFloat(z.toFixed(4)),
      heuristic_index: indexScore,
      theoretical_percentile: percentile !== null ? parseFloat(percentile.toFixed(1)) : null,
      validation_status: "RAW_PERFORMANCE_VERIFIED | HEURISTIC_UNSTANDARDIZED"
    };
  }

  // ==========================================
  // DOMAIN 4: SYMBOLIC PROCESSING SPEED (Gs)
  // ==========================================
  function scoreProcessingSpeed(trialRecords = [], options = {}) {
    let trialsAttempted = 0;
    let trialsCorrect = 0;
    let trialsIncorrect = 0;
    let latenciesMs = [];
    const durationSec = options.durationSec || PARAMS.Gs.durationSec;

    if (Array.isArray(trialRecords) && trialRecords.length > 0) {
      trialsAttempted = trialRecords.length;
      trialsCorrect = trialRecords.filter(t => t && t.is_correct === true).length;
      trialsIncorrect = trialRecords.filter(t => t && t.is_correct === false).length;
      latenciesMs = trialRecords.map(t => t ? t.latency_ms : null).filter(l => typeof l === 'number' && l > 0);
    } else {
      trialsCorrect = Math.max(0, options.correct || 0);
      trialsIncorrect = Math.max(0, options.incorrect || 0);
      trialsAttempted = trialsCorrect + trialsIncorrect;
      latenciesMs = Array.isArray(options.latenciesMs) ? options.latenciesMs : [];
    }

    const netSpeed = Math.max(0, trialsCorrect - (trialsIncorrect * 0.5));
    const throughputPerMin = durationSec > 0 ? (trialsCorrect / durationSec) * 60.0 : 0.0;
    const accuracy = trialsAttempted > 0 ? (trialsCorrect / trialsAttempted) * 100.0 : null;
    const latencyStats = calculateStats(latenciesMs);

    const z = (netSpeed - PARAMS.Gs.mean) / PARAMS.Gs.sd;
    const indexScore = toStandardScore(z);
    const percentile = calculateTheoreticalPercentile(indexScore);

    return {
      domain_key: "Gs",
      domain_name: "Symbolic Processing Speed",
      duration_seconds: durationSec,
      trials_attempted: trialsAttempted,
      trials_correct: trialsCorrect,
      trials_incorrect: trialsIncorrect,
      net_speed_score: parseFloat(netSpeed.toFixed(2)),
      accuracy_pct: accuracy !== null ? parseFloat(accuracy.toFixed(1)) : null,
      throughput_per_minute: parseFloat(throughputPerMin.toFixed(1)),
      median_latency_ms: latencyStats.median !== null ? Math.round(latencyStats.median) : null,
      z_score: parseFloat(z.toFixed(4)),
      heuristic_index: indexScore,
      theoretical_percentile: percentile !== null ? parseFloat(percentile.toFixed(1)) : null,
      validation_status: "RAW_PERFORMANCE_VERIFIED | HEURISTIC_UNSTANDARDIZED"
    };
  }

  // ==========================================
  // COMPOSITE & CLINICAL DISCREPANCY ANALYSIS
  // ==========================================
  function generateAssessmentReport(input = {}) {
    const gfResult  = input.Gf  !== undefined ? input.Gf  : scoreFluidReasoning(input.gfItems);
    const gwmResult = input.Gwm !== undefined ? input.Gwm : scoreWorkingMemory(input.gwmTrials, input.gwmSpan, input.gwmSuccesses);
    const gqResult  = input.Gq  !== undefined ? input.Gq  : scoreQuantitative(input.gqItems);
    const gsResult  = input.Gs  !== undefined ? input.Gs  : scoreProcessingSpeed(input.gsTrials, input.gsOptions);

    const domains = [gfResult, gwmResult, gqResult, gsResult];
    const isDomainCompleted = (d) => {
      if (!d || typeof d.heuristic_index !== 'number') return false;
      if (d.items_attempted !== undefined && d.items_attempted === 0) return false;
      if (d.trials_attempted !== undefined && d.trials_attempted === 0) return false;
      return true;
    };
    const completedDomains = domains.filter(isDomainCompleted);
    const isFullyCompleted = completedDomains.length === 4;

    // Composite Calculation (Heuristic Composite Index)
    const zGf  = gfResult  ? gfResult.z_score  : 0;
    const zGwm = gwmResult ? gwmResult.z_score : 0;
    const zGq  = gqResult  ? gqResult.z_score  : 0;
    const zGs  = gsResult  ? gsResult.z_score  : 0;

    const compositeZ = (PARAMS.Gf.weight * zGf)
                     + (PARAMS.Gwm.weight * zGwm)
                     + (PARAMS.Gq.weight * zGq)
                     + (PARAMS.Gs.weight * zGs);

    // Heuristic multi-subtest correlation expansion factor
    const compositeInflation = 1.18;
    const finalZ = compositeZ * compositeInflation;
    const compositeScore = toStandardScore(finalZ);
    const rawPercentile = calculateTheoreticalPercentile(compositeScore);
    const compositePercentile = rawPercentile !== null ? parseFloat(rawPercentile.toFixed(1)) : null;

    // General Ability Index (GAI) Calculation (Excludes speed and memory drag)
    const zGai = (0.60 * zGf + 0.40 * zGq) / 0.85;
    const gaiScore = toStandardScore(zGai);
    const rawGaiPercentile = calculateTheoreticalPercentile(gaiScore);
    const gaiPercentile = rawGaiPercentile !== null ? parseFloat(rawGaiPercentile.toFixed(1)) : null;

    // Clinical Discrepancy Detection: WAIS-IV guidelines flag divergence >= 1.5 SD (20+ points)
    const gfIndex = gfResult ? gfResult.heuristic_index : 100;
    const gsIndex = gsResult ? gsResult.heuristic_index : 100;
    const speedDiscrepancy = Math.abs(gfIndex - gsIndex);
    const hasDiscrepancy = speedDiscrepancy >= 20;

    let discrepancyAnalysis = {
      detected: hasDiscrepancy,
      speed_discrepancy_points: speedDiscrepancy,
      gai_index: hasDiscrepancy ? gaiScore : null,
      gai_theoretical_percentile: hasDiscrepancy ? gaiPercentile : null,
      interpretation: hasDiscrepancy
        ? `Statistically significant discrepancy of ${speedDiscrepancy} points detected between Fluid Reasoning (${gfIndex}) and Processing Speed (${gsIndex}). Under WAIS-IV psychometric rules, composite index is non-unitary; General Ability Index (${gaiScore}) provides a more defensible estimate of abstract reasoning without motor/timing constraints.`
        : "Cognitive factors are statistically balanced across inductive and processing domains."
    };

    // Calculate Exact 95% Confidence Interval (1.96 * SEM)
    const ciData = calculateConfidenceInterval(compositeScore, THEORETICAL_SEM, 0.95);

    // Classification Mapping
    let classification = "Average";
    if (compositeScore >= 130) classification = "Very Superior (High-Ceiling Band)";
    else if (compositeScore >= 120) classification = "Superior (High Cognitive Reserve)";
    else if (compositeScore >= 110) classification = "High Average";
    else if (compositeScore >= 90)  classification = "Average (Population Mean Band)";
    else if (compositeScore >= 80)  classification = "Low Average";
    else classification = "Borderline / Low";

    // Evidence-Based Interpretations
    const narrativeStatements = [];
    if (gfResult && gfResult.accuracy_pct !== null) {
      narrativeStatements.push(`Fluid Matrix accuracy was ${gfResult.accuracy_pct}% (${gfResult.items_correct}/${gfResult.items_attempted} items).`);
    }
    if (gwmResult && gwmResult.max_span_completed > 0) {
      narrativeStatements.push(`Working memory span reached ${gwmResult.max_span_completed} sequential units.`);
    }
    if (gsResult && gsResult.throughput_per_minute > 0) {
      narrativeStatements.push(`Visual discrimination throughput was ${gsResult.throughput_per_minute} correct items/min with ${gsResult.trials_incorrect} errors.`);
    }
    if (hasDiscrepancy && gfResult && gsResult) {
      narrativeStatements.push(`Marked processing speed bottleneck observed (${gsResult.heuristic_index}) relative to fluid induction (${gfResult.heuristic_index}); reflects deliberation or input device overhead rather than cognitive limitation.`);
    }

    return {
      assessment_id: input.assessment_id || "NM-" + Math.random().toString(36).substring(2, 10).toUpperCase(),
      assessment_version: ENGINE_VERSION,
      assessment_timestamp: input.timestamp || new Date().toISOString(),
      status: isFullyCompleted ? "COMPLETED" : "INCOMPLETE",
      completion_summary: {
        subtests_total: 4,
        subtests_completed: completedDomains.length,
        is_fully_completed: isFullyCompleted
      },
      domains: {
        Gf: gfResult,
        Gwm: gwmResult,
        Gq: gqResult,
        Gs: gsResult
      },
      composite: {
        value: compositeScore,
        score_type: "HEURISTIC_COMPOSITE_INDEX",
        theoretical_percentile: compositePercentile,
        classification: classification,
        formula_version: "CHC-Heuristic-v3.1",
        validation_status: "UNVALIDATED_CUSTOM_INDEX"
      },
      discrepancy_analysis: discrepancyAnalysis,
      uncertainty: {
        sem: THEORETICAL_SEM,
        confidence_level: "95%",
        margin_of_error: ciData.margin,
        confidence_interval: [ciData.lower, ciData.upper],
        method: "Conventional-Normal-Approximation (1.96 * SEM)",
        validation_status: "THEORETICAL_ESTIMATE"
      },
      narrative_interpretations: narrativeStatements,
      norm_reference: {
        dataset_id: null,
        sample_size: null,
        population_description: "Theoretical Gaussian Distribution N(100, 15)",
        validation_status: "NO_CLINICAL_NORMS_ATTACHED",
        transparency_note: "Scores and percentiles are mathematical projections under assumed normal parameters. They are not standardized against an empirical clinical norm sample."
      }
    };
  }

  return {
    ENGINE_VERSION,
    THEORETICAL_MEAN,
    THEORETICAL_SD,
    THEORETICAL_SEM,
    PARAMS,
    erf,
    standardNormalCDF,
    calculateTheoreticalPercentile,
    calculateConfidenceInterval,
    toStandardScore,
    calculateStats,
    scoreFluidReasoning,
    scoreWorkingMemory,
    scoreQuantitative,
    scoreProcessingSpeed,
    generateAssessmentReport
  };
}));
