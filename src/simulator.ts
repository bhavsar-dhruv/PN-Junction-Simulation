export interface SimulationParams {
  p_len: number; // um
  n_len: number; // um
  i_len: number; // um
  Na: number; // cm^-3
  Nd: number; // cm^-3
  temperature: number; // K
  vsweep_high: number; // V
  vn_step: number;
  materialp: string;
  taun: number; // s
  taup: number; // s
}

export function simulatePNJunction(params: SimulationParams) {
  const q = 1.602e-19; // C
  const k = 1.380649e-23; // J/K
  const eps0 = 8.854e-14; // F/cm
  const eps_r = 11.7; // Si
  const eps = eps_r * eps0;
  const T = params.temperature;
  const Vt = (k * T) / q;
  const ni = 1.5e10; // cm^-3 for Si at 300K, simplified
  const Eg = 1.12; // eV

  const Na = params.Na;
  const Nd = params.Nd;
  const Vbi = Vt * Math.log((Na * Nd) / (ni * ni));

  // Generate V sweep
  const v_step = params.vsweep_high / Math.max(1, params.vn_step - 1);
  const voltages = [];
  for (let i = 0; i < params.vn_step; i++) {
    voltages.push(i * v_step);
  }

  // IV and CV
  const Dn = 35; // cm^2/s
  const Dp = 12; // cm^2/s
  const Ln = Math.sqrt(Dn * params.taun);
  const Lp = Math.sqrt(Dp * params.taup);
  const J0 = q * ni * ni * (Dp / (Lp * Nd) + Dn / (Ln * Na));

  const ivData = voltages.map(V => ({
    voltage: V,
    current: Math.max(J0 * (Math.exp(V / Vt) - 1), 1e-20)
  }));

  const cvData = voltages.map(V => {
    const V_eff = Math.max(Vbi - V, 0.01); // Avoid division by zero
    const W = Math.sqrt((2 * eps * V_eff) / q * (1 / Na + 1 / Nd));
    return {
      voltage: V,
      capacitance: eps / W
    };
  });

  // 1D Spatial profiles at V = 0 (equilibrium)
  const V = 0;
  const W = Math.sqrt((2 * eps * (Vbi - V)) / q * (1 / Na + 1 / Nd));
  const xp = W * Nd / (Na + Nd);
  const xn = W * Na / (Na + Nd);

  const p_len_cm = params.p_len * 1e-4;
  const n_len_cm = params.n_len * 1e-4;
  
  const x_min = -p_len_cm;
  const x_max = n_len_cm;
  const num_points = 200;
  const dx = (x_max - x_min) / num_points;

  const spatialData = [];
  for (let i = 0; i <= num_points; i++) {
    const x = x_min + i * dx;
    let E = 0;
    let V_x = 0;
    let rho = 0;
    let p = 0;
    let n = 0;

    if (x < -xp) {
      E = 0;
      V_x = 0;
      rho = 0;
      p = Na;
      n = ni * ni / Na;
    } else if (x >= -xp && x <= 0) {
      E = -(q * Na / eps) * (x + xp);
      V_x = (q * Na / (2 * eps)) * Math.pow(x + xp, 2);
      rho = -q * Na;
      p = Na * Math.exp(-V_x / Vt);
      n = ni * ni / p;
    } else if (x > 0 && x <= xn) {
      E = (q * Nd / eps) * (x - xn);
      V_x = Vbi - (q * Nd / (2 * eps)) * Math.pow(xn - x, 2);
      rho = q * Nd;
      n = Nd * Math.exp(-(Vbi - V_x) / Vt);
      p = ni * ni / n;
    } else {
      E = 0;
      V_x = Vbi;
      rho = 0;
      n = Nd;
      p = ni * ni / Nd;
    }

    const Ei = -V_x;
    const Ec = Ei + Eg / 2;
    const Ev = Ei - Eg / 2;
    const Efp = -Vt * Math.log(Na / ni); // Approx
    const Efn = -Vbi - Vt * Math.log(Nd / ni); // Approx

    // Recombination rate (Shockley-Read-Hall approx)
    const R = (p * n - ni * ni) / (params.taup * (n + ni) + params.taun * (p + ni));

    // Current density (simplified drift-diffusion)
    const Jp = q * Dp * p * E / Vt; // Simplified
    const Jn = q * Dn * n * E / Vt; // Simplified
    const Jtot = Jp + Jn;

    spatialData.push({
      position: x * 1e4, // convert back to um
      Ec,
      Ev,
      Ei,
      Efp,
      Efn,
      ElectricField: E,
      Potential: V_x,
      ChargeDensity: rho,
      HoleDensity: p,
      ElectronDensity: n,
      ExcessHoleDensity: Math.max(0, p - (x < 0 ? Na : ni * ni / Nd)),
      ExcessElectronDensity: Math.max(0, n - (x > 0 ? Nd : ni * ni / Na)),
      RecombinationRate: R,
      CurrentHoles: Jp,
      CurrentElectrons: Jn,
      TotalCurrent: Jtot,
    });
  }

  return {
    ivData,
    cvData,
    spatialData
  };
}
