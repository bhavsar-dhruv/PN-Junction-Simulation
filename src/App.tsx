import React, { useState, useMemo } from 'react';
import * as Tabs from '@radix-ui/react-tabs';
import * as Slider from '@radix-ui/react-slider';
import * as Switch from '@radix-ui/react-switch';
import { simulatePNJunction, SimulationParams } from './simulator';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { cn } from './lib/utils';

function LogSlider({ label, value, min, max, step, onChange, units }: any) {
  const logMin = Math.log10(min);
  const logMax = Math.log10(max);
  const logValue = Math.log10(value);

  return (
    <div className="flex flex-col gap-2 mb-4">
      <div className="flex justify-between items-center">
        <label className="text-sm font-medium text-gray-700">{label}</label>
        <span className="text-sm text-gray-500">{value.toExponential(2)} {units}</span>
      </div>
      <Slider.Root
        className="relative flex items-center select-none touch-none w-full h-5"
        value={[logValue]}
        min={logMin}
        max={logMax}
        step={step}
        onValueChange={([v]) => onChange(Math.pow(10, v))}
      >
        <Slider.Track className="bg-gray-200 relative grow rounded-full h-[3px]">
          <Slider.Range className="absolute bg-[#699FBB] rounded-full h-full" />
        </Slider.Track>
        <Slider.Thumb
          className="block w-4 h-4 bg-[#699FBB] shadow-[0_2px_10px] shadow-blackA4 rounded-[10px] hover:bg-blue-100 focus:outline-none focus:shadow-[0_0_0_5px] focus:shadow-blackA8"
          aria-label={label}
        />
      </Slider.Root>
    </div>
  );
}

function LinearSlider({ label, value, min, max, step, onChange, units }: any) {
  return (
    <div className="flex flex-col gap-2 mb-4">
      <div className="flex justify-between items-center">
        <label className="text-sm font-medium text-gray-700">{label}</label>
        <span className="text-sm text-gray-500">{value} {units}</span>
      </div>
      <Slider.Root
        className="relative flex items-center select-none touch-none w-full h-5"
        value={[value]}
        min={min}
        max={max}
        step={step}
        onValueChange={([v]) => onChange(v)}
      >
        <Slider.Track className="bg-gray-200 relative grow rounded-full h-[3px]">
          <Slider.Range className="absolute bg-[#699FBB] rounded-full h-full" />
        </Slider.Track>
        <Slider.Thumb
          className="block w-4 h-4 bg-[#699FBB] shadow-[0_2px_10px] shadow-blackA4 rounded-[10px] hover:bg-blue-100 focus:outline-none focus:shadow-[0_0_0_5px] focus:shadow-blackA8"
          aria-label={label}
        />
      </Slider.Root>
    </div>
  );
}

export default function App() {
  const [params, setParams] = useState<SimulationParams>({
    p_len: 1,
    n_len: 1,
    i_len: 0,
    Na: 1e16,
    Nd: 1e16,
    temperature: 300,
    vsweep_high: 1,
    vn_step: 10,
    materialp: 'Silicon',
    taun: 1e-6,
    taup: 1e-6,
  });

  const [impurity, setImpurity] = useState(false);
  const [impurityLevel, setImpurityLevel] = useState(1e15);
  const [impurityDoping, setImpurityDoping] = useState('N-type');

  const data = useMemo(() => simulatePNJunction(params), [params]);

  const updateParam = (key: keyof SimulationParams, value: any) => {
    setParams(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div className="flex flex-col h-screen bg-[#f1f1f1]">
      <header className="bg-[#699FBB] text-white p-4 flex items-center justify-between shadow-md z-10">
        <div className="flex items-center gap-4">
          <img src="https://nanohub.org/app/site/media/images/PressKit/nanoHUB_logo_color.jpg" alt="nanoHUB" className="h-8 bg-white p-1 rounded" />
          <h1 className="text-xl font-semibold">PN-Junction Lab</h1>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Left Panel: Inputs */}
        <div className="w-1/3 min-w-[350px] bg-white border-r border-gray-200 flex flex-col shadow-sm z-0">
          <Tabs.Root defaultValue="structure" className="flex flex-col h-full">
            <Tabs.List className="flex shrink-0 border-b border-gray-200">
              <Tabs.Trigger value="structure" className="flex-1 px-4 py-3 text-sm font-medium text-gray-600 hover:text-gray-900 data-[state=active]:text-[#699FBB] data-[state=active]:border-b-2 data-[state=active]:border-[#699FBB] outline-none">
                Structure
              </Tabs.Trigger>
              <Tabs.Trigger value="materials" className="flex-1 px-4 py-3 text-sm font-medium text-gray-600 hover:text-gray-900 data-[state=active]:text-[#699FBB] data-[state=active]:border-b-2 data-[state=active]:border-[#699FBB] outline-none">
                Materials
              </Tabs.Trigger>
              <Tabs.Trigger value="environmental" className="flex-1 px-4 py-3 text-sm font-medium text-gray-600 hover:text-gray-900 data-[state=active]:text-[#699FBB] data-[state=active]:border-b-2 data-[state=active]:border-[#699FBB] outline-none">
                Environmental
              </Tabs.Trigger>
            </Tabs.List>

            <div className="flex-1 overflow-y-auto p-6">
              <Tabs.Content value="structure" className="outline-none">
                <LinearSlider label="P-type length" value={params.p_len} min={0.1} max={10} step={0.1} units="μm" onChange={(v: number) => updateParam('p_len', v)} />
                <LinearSlider label="N-type length" value={params.n_len} min={0.1} max={10} step={0.1} units="μm" onChange={(v: number) => updateParam('n_len', v)} />
                <LinearSlider label="Intrinsic Region length" value={params.i_len} min={0} max={10} step={0.1} units="μm" onChange={(v: number) => updateParam('i_len', v)} />
                <LogSlider label="Acceptor concentration (Na-)" value={params.Na} min={1e10} max={1e22} step={0.1} units="1/cm³" onChange={(v: number) => updateParam('Na', v)} />
                <LogSlider label="Donor concentration (Nd+)" value={params.Nd} min={1e10} max={1e22} step={0.1} units="1/cm³" onChange={(v: number) => updateParam('Nd', v)} />
              </Tabs.Content>

              <Tabs.Content value="materials" className="outline-none">
                <div className="mb-4">
                  <label className="text-sm font-medium text-gray-700 block mb-2">Material</label>
                  <select 
                    className="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#699FBB]"
                    value={params.materialp}
                    onChange={(e) => updateParam('materialp', e.target.value)}
                  >
                    <option value="Silicon">Silicon</option>
                    <option value="Germanium">Germanium</option>
                    <option value="GaAs">GaAs</option>
                  </select>
                </div>
                
                <h3 className="text-sm font-semibold text-gray-900 mt-6 mb-4">Minority carrier lifetimes</h3>
                <LogSlider label="For electrons" value={params.taun} min={1e-16} max={1e-4} step={0.1} units="s" onChange={(v: number) => updateParam('taun', v)} />
                <LogSlider label="For holes" value={params.taup} min={1e-16} max={1e-4} step={0.1} units="s" onChange={(v: number) => updateParam('taup', v)} />

                <div className="flex items-center justify-between mt-6 mb-4">
                  <label className="text-sm font-medium text-gray-700">Impurity doping in Intrinsic region</label>
                  <Switch.Root 
                    checked={impurity} 
                    onCheckedChange={setImpurity}
                    className="w-[42px] h-[25px] bg-gray-200 rounded-full relative shadow-[0_2px_10px] shadow-blackA4 focus:shadow-[0_0_0_2px] focus:shadow-black data-[state=checked]:bg-[#699FBB] outline-none cursor-default"
                  >
                    <Switch.Thumb className="block w-[21px] h-[21px] bg-white rounded-full shadow-[0_2px_2px] shadow-blackA4 transition-transform duration-100 translate-x-0.5 will-change-transform data-[state=checked]:translate-x-[19px]" />
                  </Switch.Root>
                </div>

                {impurity && (
                  <>
                    <div className="mb-4">
                      <label className="text-sm font-medium text-gray-700 block mb-2">Type of doping</label>
                      <select 
                        className="w-full border border-gray-300 rounded-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#699FBB]"
                        value={impurityDoping}
                        onChange={(e) => setImpurityDoping(e.target.value)}
                      >
                        <option value="N-type">N-type</option>
                        <option value="P-type">P-type</option>
                      </select>
                    </div>
                    <LogSlider label="Doping level" value={impurityLevel} min={1} max={1e22} step={0.1} units="1/cm³" onChange={setImpurityLevel} />
                  </>
                )}
              </Tabs.Content>

              <Tabs.Content value="environmental" className="outline-none">
                <LinearSlider label="Ambient temperature" value={params.temperature} min={100} max={500} step={1} units="K" onChange={(v: number) => updateParam('temperature', v)} />
                <LinearSlider label="Applied Voltage" value={params.vsweep_high} min={0} max={5} step={0.1} units="V" onChange={(v: number) => updateParam('vsweep_high', v)} />
                <LinearSlider label="Number of points" value={params.vn_step} min={2} max={100} step={1} units="" onChange={(v: number) => updateParam('vn_step', v)} />
              </Tabs.Content>
            </div>
          </Tabs.Root>
        </div>

        {/* Right Panel: Outputs */}
        <div className="flex-1 bg-[#dbeaf0] p-4 overflow-hidden flex flex-col">
          <Tabs.Root defaultValue="bands" className="flex flex-col h-full bg-white rounded-lg shadow-sm overflow-hidden">
            <Tabs.List className="flex shrink-0 border-b border-gray-200 overflow-x-auto">
              <Tabs.Trigger value="bands" className="px-4 py-3 text-sm font-medium text-gray-600 hover:text-gray-900 data-[state=active]:text-[#699FBB] data-[state=active]:border-b-2 data-[state=active]:border-[#699FBB] outline-none whitespace-nowrap">Energy Band</Tabs.Trigger>
              <Tabs.Trigger value="iv" className="px-4 py-3 text-sm font-medium text-gray-600 hover:text-gray-900 data-[state=active]:text-[#699FBB] data-[state=active]:border-b-2 data-[state=active]:border-[#699FBB] outline-none whitespace-nowrap">I-V</Tabs.Trigger>
              <Tabs.Trigger value="cv" className="px-4 py-3 text-sm font-medium text-gray-600 hover:text-gray-900 data-[state=active]:text-[#699FBB] data-[state=active]:border-b-2 data-[state=active]:border-[#699FBB] outline-none whitespace-nowrap">C-V</Tabs.Trigger>
              <Tabs.Trigger value="density" className="px-4 py-3 text-sm font-medium text-gray-600 hover:text-gray-900 data-[state=active]:text-[#699FBB] data-[state=active]:border-b-2 data-[state=active]:border-[#699FBB] outline-none whitespace-nowrap">Densities</Tabs.Trigger>
              <Tabs.Trigger value="charge" className="px-4 py-3 text-sm font-medium text-gray-600 hover:text-gray-900 data-[state=active]:text-[#699FBB] data-[state=active]:border-b-2 data-[state=active]:border-[#699FBB] outline-none whitespace-nowrap">Charge Density</Tabs.Trigger>
              <Tabs.Trigger value="field" className="px-4 py-3 text-sm font-medium text-gray-600 hover:text-gray-900 data-[state=active]:text-[#699FBB] data-[state=active]:border-b-2 data-[state=active]:border-[#699FBB] outline-none whitespace-nowrap">Electric Field</Tabs.Trigger>
              <Tabs.Trigger value="potential" className="px-4 py-3 text-sm font-medium text-gray-600 hover:text-gray-900 data-[state=active]:text-[#699FBB] data-[state=active]:border-b-2 data-[state=active]:border-[#699FBB] outline-none whitespace-nowrap">Potential</Tabs.Trigger>
              <Tabs.Trigger value="current" className="px-4 py-3 text-sm font-medium text-gray-600 hover:text-gray-900 data-[state=active]:text-[#699FBB] data-[state=active]:border-b-2 data-[state=active]:border-[#699FBB] outline-none whitespace-nowrap">Total Current</Tabs.Trigger>
              <Tabs.Trigger value="recombination" className="px-4 py-3 text-sm font-medium text-gray-600 hover:text-gray-900 data-[state=active]:text-[#699FBB] data-[state=active]:border-b-2 data-[state=active]:border-[#699FBB] outline-none whitespace-nowrap">Recombination</Tabs.Trigger>
              <Tabs.Trigger value="carrier" className="px-4 py-3 text-sm font-medium text-gray-600 hover:text-gray-900 data-[state=active]:text-[#699FBB] data-[state=active]:border-b-2 data-[state=active]:border-[#699FBB] outline-none whitespace-nowrap">Carrier Density</Tabs.Trigger>
            </Tabs.List>

            <div className="flex-1 p-4 overflow-y-auto">
              <Tabs.Content value="bands" className="h-full outline-none">
                <h2 className="text-lg font-semibold mb-4 text-center">Energy Band Diagram</h2>
                <ResponsiveContainer width="100%" height="90%">
                  <LineChart data={data.spatialData} margin={{ top: 5, right: 30, left: 20, bottom: 25 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="position" label={{ value: 'Position (μm)', position: 'bottom', offset: 0 }} />
                    <YAxis label={{ value: 'Energy (eV)', angle: -90, position: 'insideLeft' }} />
                    <Tooltip formatter={(value: number) => value.toExponential(2)} />
                    <Legend verticalAlign="top" height={36}/>
                    <Line type="monotone" dataKey="Ec" stroke="#1f77b4" dot={false} name="Ec" />
                    <Line type="monotone" dataKey="Ev" stroke="#1f77b4" dot={false} name="Ev" />
                    <Line type="monotone" dataKey="Ei" stroke="#AAAAAA" strokeDasharray="5 5" dot={false} name="Ei" />
                    <Line type="monotone" dataKey="Efp" stroke="#FF0000" strokeDasharray="3 3" dot={false} name="QuasiFermi Holes" />
                    <Line type="monotone" dataKey="Efn" stroke="#FF0000" strokeDasharray="3 3" dot={false} name="QuasiFermi Electrons" />
                  </LineChart>
                </ResponsiveContainer>
              </Tabs.Content>

              <Tabs.Content value="iv" className="h-full outline-none">
                <h2 className="text-lg font-semibold mb-4 text-center">I-V Characteristics</h2>
                <ResponsiveContainer width="100%" height="90%">
                  <LineChart data={data.ivData} margin={{ top: 5, right: 30, left: 20, bottom: 25 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="voltage" label={{ value: 'Gate Voltage (V)', position: 'bottom', offset: 0 }} />
                    <YAxis scale="log" domain={['auto', 'auto']} label={{ value: 'Current (A/cm²)', angle: -90, position: 'insideLeft' }} />
                    <Tooltip formatter={(value: number) => value.toExponential(2)} />
                    <Line type="monotone" dataKey="current" stroke="#1f77b4" dot={false} name="IV" />
                  </LineChart>
                </ResponsiveContainer>
              </Tabs.Content>

              <Tabs.Content value="cv" className="h-full outline-none">
                <h2 className="text-lg font-semibold mb-4 text-center">C-V Characteristics</h2>
                <ResponsiveContainer width="100%" height="90%">
                  <LineChart data={data.cvData} margin={{ top: 5, right: 30, left: 20, bottom: 25 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="voltage" label={{ value: 'Gate Voltage (V)', position: 'bottom', offset: 0 }} />
                    <YAxis scale="log" domain={['auto', 'auto']} label={{ value: 'Capacitance (F/cm²)', angle: -90, position: 'insideLeft' }} />
                    <Tooltip formatter={(value: number) => value.toExponential(2)} />
                    <Line type="monotone" dataKey="capacitance" stroke="#1f77b4" dot={false} name="CV" />
                  </LineChart>
                </ResponsiveContainer>
              </Tabs.Content>

              <Tabs.Content value="density" className="h-full outline-none">
                <h2 className="text-lg font-semibold mb-4 text-center">Doping, Electron and Hole Density</h2>
                <ResponsiveContainer width="100%" height="90%">
                  <LineChart data={data.spatialData} margin={{ top: 5, right: 30, left: 20, bottom: 25 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="position" label={{ value: 'Position (μm)', position: 'bottom', offset: 0 }} />
                    <YAxis scale="log" domain={[1e10, 'auto']} label={{ value: 'Density (/cm³)', angle: -90, position: 'insideLeft' }} />
                    <Tooltip formatter={(value: number) => value.toExponential(2)} />
                    <Legend verticalAlign="top" height={36}/>
                    <Line type="monotone" dataKey="HoleDensity" stroke="purple" dot={false} name="Hole Density" />
                    <Line type="monotone" dataKey="ElectronDensity" stroke="green" dot={false} name="Electron Density" />
                  </LineChart>
                </ResponsiveContainer>
              </Tabs.Content>

              <Tabs.Content value="charge" className="h-full outline-none">
                <h2 className="text-lg font-semibold mb-4 text-center">Net Charge Density</h2>
                <ResponsiveContainer width="100%" height="90%">
                  <LineChart data={data.spatialData} margin={{ top: 5, right: 30, left: 20, bottom: 25 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="position" label={{ value: 'Position (μm)', position: 'bottom', offset: 0 }} />
                    <YAxis label={{ value: 'Charge Density (C/cm³)', angle: -90, position: 'insideLeft' }} />
                    <Tooltip formatter={(value: number) => value.toExponential(2)} />
                    <Line type="monotone" dataKey="ChargeDensity" stroke="#1f77b4" dot={false} name="Density" />
                  </LineChart>
                </ResponsiveContainer>
              </Tabs.Content>

              <Tabs.Content value="field" className="h-full outline-none">
                <h2 className="text-lg font-semibold mb-4 text-center">Electric Field</h2>
                <ResponsiveContainer width="100%" height="90%">
                  <LineChart data={data.spatialData} margin={{ top: 5, right: 30, left: 20, bottom: 25 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="position" label={{ value: 'Position (μm)', position: 'bottom', offset: 0 }} />
                    <YAxis label={{ value: 'Electric Field (V/cm)', angle: -90, position: 'insideLeft' }} />
                    <Tooltip formatter={(value: number) => value.toExponential(2)} />
                    <Line type="monotone" dataKey="ElectricField" stroke="#1f77b4" dot={false} name="Electric Field" />
                  </LineChart>
                </ResponsiveContainer>
              </Tabs.Content>

              <Tabs.Content value="potential" className="h-full outline-none">
                <h2 className="text-lg font-semibold mb-4 text-center">Electric Potential</h2>
                <ResponsiveContainer width="100%" height="90%">
                  <LineChart data={data.spatialData} margin={{ top: 5, right: 30, left: 20, bottom: 25 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="position" label={{ value: 'Position (μm)', position: 'bottom', offset: 0 }} />
                    <YAxis label={{ value: 'Potential (V)', angle: -90, position: 'insideLeft' }} />
                    <Tooltip formatter={(value: number) => value.toExponential(2)} />
                    <Line type="monotone" dataKey="Potential" stroke="#1f77b4" dot={false} name="Potential" />
                  </LineChart>
                </ResponsiveContainer>
              </Tabs.Content>

              <Tabs.Content value="current" className="h-full outline-none">
                <h2 className="text-lg font-semibold mb-4 text-center">Total, Electron and Hole Current</h2>
                <ResponsiveContainer width="100%" height="90%">
                  <LineChart data={data.spatialData} margin={{ top: 5, right: 30, left: 20, bottom: 25 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="position" label={{ value: 'Position (μm)', position: 'bottom', offset: 0 }} />
                    <YAxis label={{ value: 'Current Density (A/cm²)', angle: -90, position: 'insideLeft' }} />
                    <Tooltip formatter={(value: number) => value.toExponential(2)} />
                    <Legend verticalAlign="top" height={36}/>
                    <Line type="monotone" dataKey="CurrentHoles" stroke="purple" dot={false} name="Total Current Holes" />
                    <Line type="monotone" dataKey="CurrentElectrons" stroke="green" dot={false} name="Total Current Electrons" />
                    <Line type="monotone" dataKey="TotalCurrent" stroke="blue" strokeDasharray="5 5" dot={false} name="Total Current" />
                  </LineChart>
                </ResponsiveContainer>
              </Tabs.Content>

              <Tabs.Content value="recombination" className="h-full outline-none">
                <h2 className="text-lg font-semibold mb-4 text-center">Recombination Rate</h2>
                <ResponsiveContainer width="100%" height="90%">
                  <LineChart data={data.spatialData} margin={{ top: 5, right: 30, left: 20, bottom: 25 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="position" label={{ value: 'Position (μm)', position: 'bottom', offset: 0 }} />
                    <YAxis label={{ value: 'Recombination Rate (/cm³s)', angle: -90, position: 'insideLeft' }} />
                    <Tooltip formatter={(value: number) => value.toExponential(2)} />
                    <Line type="monotone" dataKey="RecombinationRate" stroke="#1f77b4" dot={false} name="Recombination Rate" />
                  </LineChart>
                </ResponsiveContainer>
              </Tabs.Content>

              <Tabs.Content value="carrier" className="h-full outline-none">
                <h2 className="text-lg font-semibold mb-4 text-center">Carrier Density</h2>
                <ResponsiveContainer width="100%" height="90%">
                  <LineChart data={data.spatialData} margin={{ top: 5, right: 30, left: 20, bottom: 25 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="position" label={{ value: 'Position (μm)', position: 'bottom', offset: 0 }} />
                    <YAxis scale="log" domain={[1, 'auto']} label={{ value: 'Carrier Density (/cm³)', angle: -90, position: 'insideLeft' }} />
                    <Tooltip formatter={(value: number) => value.toExponential(2)} />
                    <Legend verticalAlign="top" height={36}/>
                    <Line type="monotone" dataKey="ExcessElectronDensity" stroke="purple" dot={false} name="Excess Electron Density" />
                    <Line type="monotone" dataKey="ExcessHoleDensity" stroke="green" dot={false} name="Excess Hole Density" />
                  </LineChart>
                </ResponsiveContainer>
              </Tabs.Content>

            </div>
          </Tabs.Root>
        </div>
      </div>
    </div>
  );
}
