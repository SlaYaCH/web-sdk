/** Presentation only. Feed one FINAL result per paid round, never intermediate SDK events. */
export function createSideReactionDirector(duo, options = {}) {
 const cfg = { noWinStreak: 10, minWinMultiplier: 5, celebrateMultiplier: 20,
  occasionalChance: 0.12, occasionalCooldownRounds: 8, winCooldownRounds: 4,
  random: Math.random, ...options };
 let round = 0, streak = 0, frustrationShown = false;
 let lastOccasional = -cfg.occasionalCooldownRounds, lastWin = -cfg.winCooldownRounds, nextActor = 'ler';
 const seen = new Set();
 const snapshot = () => ({ round, noWinStreak: streak, frustrationShown });
 function result(reason, reaction = null, target = null, shown = false) {
  return { ...snapshot(), reason, reaction, target, shown };
 }
 function play(kind, nowMs, target = 'both') {
  return result('reaction', kind, target, duo.react(kind, nowMs, { target }));
 }
 return {
  snapshot,
  onBonus({ eventId, nowMs } = {}) {
   if(typeof eventId!=='string'||!eventId) throw new Error('A unique bonus eventId string is required.');
   const key='bonus:'+eventId;
   if(seen.has(key))return result('duplicate');
   seen.add(key);if(seen.size>256)seen.delete(seen.values().next().value);
   streak=0;frustrationShown=false;
   return play('bonus',nowMs);
  },
  reset() { round=0;streak=0;frustrationShown=false;lastOccasional=-cfg.occasionalCooldownRounds;lastWin=-cfg.winCooldownRounds;nextActor='ler';seen.clear(); },
  onRound({ roundId, payoutMultiplier, bonusTriggered = false, isBonusRound = false, nowMs } = {}) {
   if (typeof roundId !== 'string' || !roundId) throw new Error('A unique roundId string is required.');
   if (!Number.isFinite(payoutMultiplier) || payoutMultiplier < 0) throw new Error('payoutMultiplier must be the non-negative final payout / bet.');
   if (seen.has(roundId)) return result('duplicate');
   seen.add(roundId); if(seen.size>256) seen.delete(seen.values().next().value);
   // Bonus celebration takes precedence over every monetary result.
   if (bonusTriggered) { streak=0;frustrationShown=false;return play('bonus',nowMs); }
   if (isBonusRound) return result('bonus-round-ignored');
   round++;
   if (payoutMultiplier > 0) {
    streak=0;frustrationShown=false;
    if(payoutMultiplier < cfg.minWinMultiplier) return result('small-win-idle');
    if(round-lastWin < cfg.winCooldownRounds) return result('win-cooldown');
    lastWin=round;
    return play(payoutMultiplier >= cfg.celebrateMultiplier ? 'celebrate' : 'win',nowMs);
   }
   streak++;
   if(streak >= cfg.noWinStreak && !frustrationShown) {
    frustrationShown=true;lastOccasional=round;
    return play('frustrated',nowMs);
   }
   // No repeated frustration or shrug after the threshold until a paying round resets the streak.
   if(streak >= cfg.noWinStreak) return result('streak-already-reacted');
   if(streak >= 3 && round-lastOccasional >= cfg.occasionalCooldownRounds && cfg.random() < cfg.occasionalChance) {
    lastOccasional=round;const target=nextActor;nextActor=nextActor==='ler'?'inso':'ler';
    return play('noWin',nowMs,target);
   }
   return result('no-win-idle');
  }
 };
}
