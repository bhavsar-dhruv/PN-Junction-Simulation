import os
if 'SESSIONDIR' not in os.environ:
    os.environ['SESSIONDIR'] = '.'
    f = open("./resources", "wt")
    f.write("sessionid 0\n")
    f.write("filexfer_cookie a\n")
    f.write("filexfer_port 10\n")    
    f.close()
from sim2lbuilder import *
schema = GetSimtoolDefaultSchema("st4pnjunction")
import nanohubuidl.teleport as t
from nanohubuidl.material import MaterialBuilder
from nanohubuidl.material import MaterialContent
from nanohubuidl.plotly import PlotlyBuilder
from nanohubuidl.app import AppBuilder, FormHelper
from nanohubuidl.nanohub import Auth

schema["inputs"]['Na']['units'] = "1/cm^3"
schema["inputs"]['Na']['max'] = 1e+22
schema["inputs"]['Na']['label'] = 'Acceptor concentration'
schema["inputs"]['Nd']['units'] = "1/cm^3"
schema["inputs"]['Nd']['max'] = 1e+22
schema["inputs"]['Nd']['label'] = 'Donor concentration'
schema["inputs"]['taun']['units'] = "s"
schema["inputs"]['taun']['label'] = 'For electrons'
schema['inputs']['taun']['min'] = 1e-16
schema['inputs']['taup']['min'] = 1e-16
schema["inputs"]['taup']['units'] = "s"
schema["inputs"]['taup']['label'] = 'For holes'
schema['inputs']['taun']['max'] = 1e-4
schema['inputs']['taup']['max'] = 1e-4
schema["inputs"]['i_len']['units'] = "μm"
schema["inputs"]['i_len']['label'] = 'Intrinsic Region length'
schema["inputs"]['n_len']['units'] = "μm"
schema["inputs"]['n_len']['label'] = 'N-type length'
schema["inputs"]['p_len']['units'] = "μm"
schema["inputs"]['p_len']['label'] = 'P-type length'
schema["inputs"]['temperature']['units'] = "K"
schema["inputs"]['impuritylevel']['label'] = 'Doping level'
schema["inputs"]['impuritylevel']['units'] = "1/cm^3"
schema["inputs"]['impuritylevel']['min'] = 1
schema["inputs"]['p_node']['label'] = 'P-type Nodes'
schema["inputs"]['i_node']['label'] = 'Intrinsic Nodes'
schema["inputs"]['n_node']['label'] = 'N-type Nodes'
schema["inputs"]['impurity']['label'] = 'Impurity doping in Intrinsic region.'
schema["inputs"]['temperature']['label'] = 'Ambient temperature'
schema["inputs"]['vsweep_high']['label'] = 'Applied Voltage'
schema["inputs"]['vn_step']['label'] = 'Number of points'
schema["inputs"]['impuritydoping']['label'] = 'Type of doping'
schema["inputs"]['materialp']['label'] = 'Material'

s = UIDLConstructor(
    schema,
    width="99.8vw", 
    height="99.8vh", 
    load_default=True,
    delay = 1000
)

s.theme = MaterialBuilder.DefaultTheme(
    primary_color = '#699FBB',
    secondary_color = '#f1f1f1',
    primary_bg = '#FFFFFF',
    secondary_bg = '#dbeaf0',
    default_button = 'rgba(255, 255, 255, 0.87)',
    primary_button = 'rgba(255, 255, 255, 0.87)',
    secondary_button = 'rgba(0, 0, 0, 0.87)',
    default_button_bg = 'rgb(63, 162, 192)',
    primary_button_bg = 'rgba(0, 0, 0, 0.65)',
    secondary_button_bg = 'rgba(255, 0, 0, 0.12)',
    drawer_position = "relative"
)

s.theme['components']['MuiToggleButtonGroup'] = {
    "styleOverrides": {
        "root" : {
            "BackgroundColor" : "#EEE",
        },
        "grouped" : {
            "backgroundColor":"#FFF",
            "textTransform":"none",
            "borderRadius":"20px",
            "margin":"5px",
            "&:not(:last-of-type)":{
                "borderRadius":"20px",
                "border":"1px solid #333",
            },
            "&:not(:first-of-type)":{
                "borderRadius":"20px",
                "marginTop":"5px",
                "border":"1px solid #333",
            }
        }
    }
}
    
s.theme['components']['MuiToggleButton'] = {
    "styleOverrides": {
        "root" : {
            "&.Mui-selected": {"backgroundColor": "#97aad1"},
            "&:hover": {"backgroundColor": "#EEE"},
        },
    }
}


s.inputs_layout = {
    'type': 'tab',
    'id': '',
    'label': '',
    'layout': 'horizontal',
    'children': [
        {
            'type': 'group',
            'label': 'Structure',
            'enable': None,
            'layout': 'horizontal',
            'children': [
                {'type': 'number', 'id': 'p_len','label': 'P-type length','enable': None}, 
                {'type': 'integer', 'id': 'p_node','label': 'P-type Nodes','enable': None}, 
                {'type': 'number', 'id': 'i_len','label': 'Intrinsic Region length','enable': None}, 
                {'type': 'integer', 'id': 'i_node','label': 'Intrinsic Nodes','enable': None}, 
                {'type': 'number', 'id': 'n_len','label': 'N-type length','enable': None}, 
                {'type': 'integer', 'id': 'n_node','label': 'N-type Nodes','enable': None}, 
                {'type': 'number', 'id': 'Na','label': 'Acceptor concentration (Na-)','enable': None}, 
                {'type': 'number', 'id': 'Nd','label': 'Donor concentration (Nd+)','enable': None},
            ]
        },
        {
            'type': 'group',
            'label': 'Materials',
            'enable': None,
            'layout': 'horizontal',
            'children': [
                {'type': 'choice','id': 'materialp','label': 'Material','enable': None},
                {
                    'type':'group',
                    'label':'Minority carrier lifetimes',
                    'enable':None,
                    'layout':'horizontal',
                    'children': [
                        {'type': 'number','id': 'taun','label': 'For electrons','enable': None}, 
                        {'type': 'number','id': 'taup','label': 'For holes','enable': None}
                    ] 
                }, 
                {'type': 'boolean','id': 'impurity','label': 'Impurity doping in Intrinsic region.','enable': None },
                {'type':'choice','id':'impuritydoping','label':'Type of doping','enable': [{'operand': 'parameters.impurity','operator': '==','value': True,'condition': ''}]},
                {'type':'number','id':'impuritylevel','label':'Doping level','enable': [{'operand': 'parameters.impurity','operator': '==','value': True,'condition': ''}]},
            ]
        },
        {
        'type': 'group',
        'label': 'Environmental',
        'enable': None,
        'layout': 'horizontal',
        'children': [
            {'type': 'number','id': 'temperature','label': 'Ambient temperature','enable': None}, 
            {'type': 'number','id': 'vsweep_high','label': 'Applied Voltage','enable': None}, 
            {'type': 'integer','id': 'vn_step','label': 'Number of points','enable': None}
        ]
   }]
}

'''MYTOOLNAME = "PNJUNCTIONAPP.HTML"
simToolName = 'st4pnjunction'
simToolLocation = searchForSimTool(simToolName)
inputsSchema = getSimToolInputs(simToolLocation)
outputsSchema = getSimToolOutputs(simToolLocation)
SCHEMA = {
    'name': simToolName,
    'revision': simToolLocation['simToolRevision'],
    'description': '',
    'inputs': {
        input: {k: inputsSchema[input][k]
                for k in inputsSchema[input]}
        for input in inputsSchema
    },
    'outputs': {
        output: {k: outputsSchema[output][k]
                  for k in outputsSchema[output]}
        for output in outputsSchema
    }
}
    
for input in inputsSchema:
    SCHEMA["inputs"][input] = {}
    SCHEMA["inputs"][input]["disable_fix"] = True
    SCHEMA["inputs"][input]["units"] = ""
    SCHEMA["inputs"][input]["description"] = ""
    for k in inputsSchema[input]:
        try:
            json.dumps(inputsSchema[input][k])
        except:
            inputsSchema[input][k] = str(inputsSchema[input][k])
        if k == "value":
            SCHEMA["inputs"][input]["default_value"] = inputsSchema[input][k]
        else:
            SCHEMA["inputs"][input][k] = inputsSchema[input][k]
    if 'label' not in SCHEMA["inputs"][input] or SCHEMA["inputs"][input]["label"] == "":
        SCHEMA["inputs"][input]["label"] = SCHEMA["inputs"][input]["description"]

''';


import numpy as np
import math
Paper = t.TeleportElement(MaterialContent(elementType="Paper"))
component = t.TeleportComponent("SliderCustomNumberComponent", Paper)

if ("value" not in component.propDefinitions):
    component.addPropVariable("value", {"type":"float", "defaultValue": 1})
if ("step" not in component.propDefinitions):
    component.addPropVariable("step", {"type":"float", "defaultValue": 0.1})
if ("min" not in component.propDefinitions):
    component.addPropVariable("min", {"type":"float", "defaultValue": 1})
if ("max" not in component.propDefinitions):
    component.addPropVariable("max", {"type":"float", "defaultValue": 100})
if ("variant" not in component.propDefinitions):
    component.addPropVariable("variant", {"type":"string", "defaultValue": "variant"})
if ("label" not in component.propDefinitions):
    component.addPropVariable("label", {"type":"string", "defaultValue": ""})
if ("description" not in component.propDefinitions):
    component.addPropVariable("description", {"type":"string", "defaultValue": ""})
if ("valueLabelDisplay" not in component.propDefinitions):
    component.addPropVariable("valueLabelDisplay", {"type":"string", "defaultValue": "auto"})

if ("scale10" not in component.propDefinitions):
    component.addPropVariable("scale10", {"type":"func", 'defaultValue' : "(x)=>{ return (Math.pow(10, Math.trunc(x))*(((x%1).toFixed(1)>0)?((x%1).toFixed(1)*10):1)).toExponential(2)}"})  
if ("unscale10" not in component.propDefinitions):
    component.addPropVariable("unscale10", {"type":"func", 'defaultValue' : "(x)=>{ let vlog = Math.log10(x); let v = Math.trunc(vlog); return v + Math.trunc(10**(vlog-v))%10/10;}"})  
if ("marks" not in component.propDefinitions):
    eol = "\n";
    js = ""
    js += "( self ) => {" + eol
    js += "  let t = Math.log10(self.props.max); " + eol
    js += "  let b = Math.log10(self.props.min);" + eol
    js += "  let s = self.props.step * 10;" + eol
    js += "  let a = Array(Math.ceil((t - b) / s)).fill(b).map((x, y) => x + y * s); " + eol
    js += "  let m = a.map((x) => { return {'value': x,'label':'e^'+ x} });" + eol
    js += "  return m;" + eol
    js += "}" + eol
    component.addPropVariable("marks", {"type":"func", 'defaultValue' : js})  
if ("onChange" not in component.propDefinitions):
    component.addPropVariable("onChange", {"type":"func", 'defaultValue' : "(x)=>{ }"})  

if ("slidertip" not in component.propDefinitions):
    eol = "\n";
    js =  "(props)=>{" + eol
    js += "  const { children, open, value } = props;" + eol
    js += "  return React.createElement(Material.Tooltip,{" + eol
    js += "    'open':open,'enterTouchDelay':0,'placement':'top', 'title':value" + eol
    js += "  }, children);" + eol
    js += "}" + eol
    component.addPropVariable("slidertip", {"type":"func", 'defaultValue' : js})  

FormControl = t.TeleportElement(MaterialContent(elementType="FormControl"))
FormControl.content.attrs["variant"] = {
  "type": "dynamic",
  "content": {
    "referenceType": "prop",
    "id": "variant"
  }  
}        
FormControl.content.style = {
    "border":"1px solid rgba(0, 0, 0, 0.23)", 
    "borderRadius":"4px", 
    "paddingLeft" : "14px",
    "paddingRight" : "14px",
    "paddingTop" : "4px",
    "paddingBottom" : "4px",

}
slider = t.TeleportElement(MaterialContent(elementType="Slider"))
InputLabel = t.TeleportElement(MaterialContent(elementType="InputLabel"))
InputLabel.content.attrs["htmlFor"]="component-filled"
InputLabel.content.attrs["shrink"] = True

InputLabel.content.style = { "background":"white", "padding":"3px", "top" : "-10px", "left" : "10px"}    
InputLabelText = t.TeleportDynamic(content={"referenceType": "prop","id": "label"})
FormHelperText = t.TeleportElement(MaterialContent(elementType="FormHelperText"))
FormHelperText.addContent(t.TeleportDynamic(content={"referenceType": "prop","id": "description"}))
FormHelperText.content.style = {
    "marginLeft" : "14px",
    "marginRight" : "14px",
}   

slider.content.events["change"] = []
slider.content.events["change"].append({
    "type": "propCall2",
    "calls": "onChange",
    "args": ["{'target':{'value':self.props.scale10(arguments[1])}}"]
})

slider.content.attrs["value"] = "$self.props.unscale10(self.props.value)"
slider.content.attrs["defaultValue"] = 10
slider.content.attrs["valueLabelDisplay"] = {
  "type": "dynamic",
  "content": {
    "referenceType": "prop",
    "id": "valueLabelDisplay"
  }  
}
slider.content.attrs["valueLabelFormat"] = {
  "type": "dynamic",
  "content": {
    "referenceType": "prop",
    "id": "scale10"
  }  
}      
slider.content.attrs["getAriaValueText"] = {
  "type": "dynamic",
  "content": {
    "referenceType": "prop",
    "id": "getAriaValueText"
  }  
}  
slider.content.attrs["ValueLabelComponent"] = {
  "type": "dynamic",
  "content": {
    "referenceType": "prop",
    "id": "ValueLabelComponent"
  }  
}  

slider.content.attrs["step"] = "$self.props.step"
slider.content.attrs["min"] = "$Math.log10(self.props.min)"
slider.content.attrs["max"] = "$Math.log10(self.props.max)"

slider.content.attrs["marks"] = "$self.props.marks(self)"

InputLabel.addContent(InputLabelText)

FormControl.addContent(InputLabel)
FormControl.addContent(slider)
Paper.addContent(FormControl)
Paper.addContent(FormHelperText)
Paper.content.style = {
    "width":"100%",
    "display": "flex", 
    "flexDirection": "column", 
    "paddingBottom": "14px", 
}
    
s.components["SliderCustomNumberComponent"] = component 




Na = t.TeleportElement(t.TeleportContent(elementType="SliderCustomNumberComponent"))
Na.content.attrs['label'] = schema['inputs']['Na']['label'], 
Na.content.attrs['description'] = schema['inputs']['Na']['description'], 
Na.content.attrs['value'] = {
    "type": "dynamic",
    "content": {
        "referenceType": "state",
        "id": "Na"
    }
}
Na.content.attrs['units'] = schema['inputs']['Na']['units']
Na.content.attrs['min'] = schema['inputs']['Na']['min']
Na.content.attrs['max'] = schema['inputs']['Na']['max']
Na.content.events = {'onChange':[{ "type": "stateChange", "modifies": "Na","newState": "$e.target.value"},{'type': 'propCall2', 'calls': 'onChange', 'args': ["{'Na':e.target.value}"]}]}
s.params['Na'] = Na

Nd = t.TeleportElement(t.TeleportContent(elementType="SliderCustomNumberComponent"))
Nd.content.attrs['label'] = schema['inputs']['Nd']['label'], 
Nd.content.attrs['description'] = schema['inputs']['Nd']['description'], 
Nd.content.attrs['value'] = {
    "type": "dynamic",
    "content": {
        "referenceType": "state",
        "id": "Nd"
    }
}
Nd.content.attrs['units'] = schema['inputs']['Nd']['units']
Nd.content.attrs['min'] = schema['inputs']['Nd']['min']
Nd.content.attrs['max'] = schema['inputs']['Nd']['max']
Nd.content.events = {'onChange':[{ "type": "stateChange", "modifies": "Nd","newState": "$e.target.value"},{'type': 'propCall2', 'calls': 'onChange', 'args': ["{'Nd':e.target.value}"]}]}
s.params['Nd'] = Nd







taup = t.TeleportElement(t.TeleportContent(elementType="SliderCustomNumberComponent"))
taup.content.attrs['label'] = schema['inputs']['taup']['label'], 
taup.content.attrs['description'] = schema['inputs']['taup']['description'], 
taup.content.attrs['value'] = {
    "type": "dynamic",
    "content": {
        "referenceType": "state",
        "id": "taup"
    }
}
taup.content.attrs['units'] = schema['inputs']['taup']['units']
taup.content.attrs['min'] = schema['inputs']['taup']['min']
taup.content.attrs['max'] = schema['inputs']['taup']['max']
taup.content.events = {'onChange':[{ "type": "stateChange", "modifies": "taup","newState": "$e.target.value"},{'type': 'propCall2', 'calls': 'onChange', 'args': ["{'taup':e.target.value}"]}]}
taup.content.attrs["scale10"] = "$(x)=>{ return Math.pow(10,x).toExponential(2); }"  
taup.content.attrs["unscale10"] = "$(x)=>{ return Math.log10(x); }"
taup.content.attrs["step"] = 0.1
s.params['taup'] = taup


taun = t.TeleportElement(t.TeleportContent(elementType="SliderCustomNumberComponent"))
taun.content.attrs['label'] = schema['inputs']['taun']['label'], 
taun.content.attrs['description'] = schema['inputs']['taun']['description'], 
taun.content.attrs['value'] = {
    "type": "dynamic",
    "content": {
        "referenceType": "state",
        "id": "taun"
    }
}
taun.content.attrs['units'] = schema['inputs']['taun']['units']
taun.content.attrs['min'] = schema['inputs']['taun']['min']
taun.content.attrs['max'] = schema['inputs']['taun']['max']
taun.content.events = {'onChange':[{ "type": "stateChange", "modifies": "taun","newState": "$e.target.value"},{'type': 'propCall2', 'calls': 'onChange', 'args': ["{'taun':e.target.value}"]}]}
taun.content.attrs["scale10"] = "$(x)=>{ return Math.pow(10,x).toExponential(2); }"  
taun.content.attrs["unscale10"] = "$(x)=>{ return Math.log10(x); }"
taun.content.attrs["step"] = 0.1

s.params['taun'] = taun


[{'operand': 'lastDefault','operator': '==','value': True,'condition': ''}]

impuritylevel = t.TeleportElement(t.TeleportContent(elementType="SliderCustomNumberComponent"))
impuritylevel.content.attrs['label'] = schema['inputs']['impuritylevel']['label'], 
impuritylevel.content.attrs['description'] = schema['inputs']['impuritylevel']['description'], 
impuritylevel.content.attrs['value'] = {
    "type": "dynamic",
    "content": {
        "referenceType": "state",
        "id": "impuritylevel"
    }
}
impuritylevel.content.attrs['units'] = schema['inputs']['impuritylevel']['units']
impuritylevel.content.attrs['min'] = schema['inputs']['impuritylevel']['min']
impuritylevel.content.attrs['max'] = schema['inputs']['impuritylevel']['max']
impuritylevel.content.events = {'onChange':[{ "type": "stateChange", "modifies": "impuritylevel","newState": "$e.target.value"},{'type': 'propCall2', 'calls': 'onChange', 'args': ["{'impuritylevel':e.target.value}"]}]}

s.params['impuritylevel'] = impuritylevel


paper2 = t.TeleportElement(MaterialContent(elementType="ToggleButton"))
component2 = t.TeleportComponent("ToogleCustomComponent", paper2)
if ("value" not in component2.propDefinitions):
    component2.addPropVariable("value", {"type":"float", "defaultValue": 1})
if ("label" not in component2.propDefinitions):
    component2.addPropVariable("label", {"type":"string", "defaultValue": ""})
if ("onChange" not in component2.propDefinitions):
    component2.addPropVariable("onChange", {"type":"func", 'defaultValue' : "(x)=>{ }"}) 
Icon2 = t.TeleportElement(MaterialContent(elementType="Icon"))
IconText2 = t.TeleportStatic(content="check")
CIconText2 = t.TeleportConditional(IconText2)
CIconText2.reference = {
    "type": "dynamic",
    "content": {
        "referenceType": "prop",
        "id": "value"
    }
}
CIconText2.value = True
CIconText2.conditions =[{"operation" : "=="}]

Icon2.addContent(CIconText2)   
Icon2.content.style = {
    "height" : "20px",
    "width" : "50px"
}
paper2.addContent(Icon2)
paper2.addContent(t.TeleportDynamic(content={
        "referenceType": "prop",
        "id": "label"
    })) 
paper2.content.attrs["value"] = {
    "type": "dynamic",
    "content": {
        "referenceType": "prop",
        "id": "value"
    }
}
paper2.content.style = {
    "width" : "100%"
}
paper2.content.attrs["size"] = "small"
paper2.content.attrs["variant"] = "filled"
paper2.content.events['click'] = [
    {'type': 'propCall2', 'calls': 'onChange', 'args': ['!self.props.value']}
]
s.components["ToogleCustomComponent"] = component2

impurity = t.TeleportElement(t.TeleportContent(elementType="ToogleCustomComponent"))
impurity.content.attrs['label'] = schema['inputs']['impurity']['label'], 
impurity.content.attrs['value'] = {
    "type": "dynamic",
    "content": {
        "referenceType": "state",
        "id": "impurity"
    }
}
impurity.content.events = {'onChange':[{ "type": "stateChange", "modifies": "impurity","newState": "$toogle"},{'type': 'propCall2', 'calls': 'onChange', 'args': ["{'impurity':self.state.impurity}"]}]}
s.params['impurity'] = impurity




IV = {
    'id': 'iv',
    'title' : 'I-V Characteristics',
    'function': 'loadPlotly',
    'dataset': {
        'IV Characteristic': {
            'name' : 'IV', 
            'x': '$voltage',
            'y': '$function',
            'line' : {
              'color' :'#1f77b4'
            },
        }
    },
    'layout': {
        'title': 'IV Characteristics',
        'showlegend': False,
        'yaxis': {
            'title': 'Current(A/cm^2)',
            'exponentformat':'e',
            'type': 'log',
        },
        'xaxis': {
            'title': 'Gate Voltage (V)',
        },
        'updatemenus': [
            {
                'buttons' : [
                    {
                        'label':"   (x)",
                        'method':"relayout",
                        'args':["xaxis", {'type':'linear'}],
                    },{
                        'label':"log(x)",
                        'method':"relayout",
                        'args':["xaxis", {'type':'log'}],
                    }
                ],
                'direction':"right",
                'pad':{"r": 0, "t": 0},
                'showactive':False,
                'x':0,
                'xanchor':"left",
                'y':-0.04,
                'yanchor':"top"
            },
            {
                'buttons':[
                    {
                        'label':"log(y)",
                        'method':"relayout",
                        'args':["yaxis", {'type':'log'}],
                    },
                    {
                        'label':"   (y)",
                        'method':"relayout",
                        'args':["yaxis", {'type':'linear'}],
                    }
                ],
                'direction':"right",
                'pad':{"r": 0, "t": 0},
                'showactive':False,
                'x':-0.07,
                'xanchor':"left",
                'y':0.09,
                'yanchor':"top"
            },
        ]
    },
}

CV = {
    'id': 'cv',
    'function': 'loadPlotly',
    'title' : 'C-V Characteristics',
    'dataset': {
        'CV Characteristic': {
            'name' : 'CV', 
            'x': '$voltage',
            'y': '$function',
            'line' : {
              'color' :'#1f77b4'
            },
        }
    },
    'layout': {
        'title': 'CV Characteristics',
        'showlegend': False,
        'yaxis': {
            'title': 'Capacitance(F/cm^2)',
            'exponentformat':'e',
            'type' : 'log'
        },
        'xaxis': {
            'title': 'Gate Voltage (V)',
        },'updatemenus': [
            {
                'buttons' : [
                    {
                        'label':"   (x)",
                        'method':"relayout",
                        'args':["xaxis", {'type':'linear'}],
                    },{
                        'label':"log(x)",
                        'method':"relayout",
                        'args':["xaxis", {'type':'log'}],
                    }
                ],
                'direction':"right",
                'pad':{"r": 0, "t": 0},
                'showactive':False,
                'x':0,
                'xanchor':"left",
                'y':-0.04,
                'yanchor':"top"
            },
            {
                'buttons':[
                    {
                        'label':"log(y)",
                        'method':"relayout",
                        'args':["yaxis", {'type':'log'}],
                    },{
                        'label':"   (y)",
                        'method':"relayout",
                        'args':["yaxis", {'type':'linear'}],
                    }
                ],
                'direction':"right",
                'pad':{"r": 0, "t": 0},
                'showactive':False,
                'x':-0.07,
                'xanchor':"left",
                'y':0.09,
                'yanchor':"top"
            },
        ]
    },
}

ChargeDensity = {
    'id': 'net',
    'title': 'Charge Density',
    'function': 'loadSequencePlotly',
    'dataset': {
        'Net Charge Density': {
            'name': 'Density',
            'x': '$position',
            'y': '$function',
            'line': {
                'color': '#1f77b4'
            },
        }
    },
    'layout': {
        'title': 'Net Charge Density',
        'showlegend': False,
        'yaxis': {
            'title': 'Charge Density (C\cm3)',
            'exponentformat': 'e'
        },
        'xaxis': {
            'title': 'Position(um)'
        }
    },
    'normalize': True,
    'start_trace': 0,
}


BANDS = {
    'id': 'bands',
    'title': 'Energy Band',
    'function': 'loadSequencePlotly',
    'dataset': {
        'Ec': {
            'name': 'Ec',
            'x': '$position',
            'y': '$function',
            'line': {
                'color': '#1f77b4'
            },
        },
        'Ev': {
            'name': 'Ev',
            'x': '$position',
            'y': '$function',
            'line': {
                'color': '#1f77b4'
            },
        },
        'Ei': {
            'name': 'Ei',
            'x': '$position',
            'y': '$function',
            'line': {
                'color': '#AAAAAA',
                'dash' : 'dashdot'
            },
        },
        'QuasiFermi Holes': {
            'name': 'QuasiFermi Holes',
            'x': '$position',
            'y': '$function',
            'line': {
                'color': '#FF0000',
                'dash' : 'dot'
            },
        },
        'QuasiFermi Electrons': {
            'name': 'QuasiFermi Electrons',
            'x': '$position',
            'y': '$function',
            'line': {
                'color': '#FF0000',
                'dash' : 'dot'
            },
        }
    },
    'layout': {
        'title': 'Energy Band Diagram',
        'showlegend': False,
        'yaxis': {
            'title': 'Energy (eV)',
            'exponentformat': 'e'
        },
        'xaxis': {
            'title': 'Position(um)'
        }
    },
    'normalize': True,
    'start_trace': 0,
}

TOTALCURRENT = {
    'id': 'current',
    'title' : 'Total Current',
    'function': 'loadSequencePlotly',
    'dataset': {
        'Total Current Holes': {
            'name': 'Total Current Holes',
            'x': '$position',
            'y': '$function',
            'line': {
                'color': 'purple'
            },
        },
        'Total Current Electrons': {
            'name': 'Total Current Electrons',
            'x': '$position',
            'y': '$function',
            'line': {
                'color': 'green'
            },
        },
        'Total Current': {
            'name': 'Total Current',
            'x': '$position',
            'y': '$function',
            'line': {
                'color': 'blue',
                'dash': 'dash'
            },
        }
    },
    'layout': {
        'title': 'Total, Electron and Hole Current',
        'showlegend': False,
        'yaxis': {
            'type': 'log',
            'title': 'Current Density (\cm3)',
            'exponentformat': 'e'
        },
        'xaxis': {
            'title': 'Position(um)'
        }
    },
    'normalize': True,
    'start_trace': 1,
}

DENSITY = {
    'id': 'density',
    'function': 'loadSequencePlotly',
    'title':'Total Density',
    'dataset': {
        'Hole Density': {
            'name': 'Hole Density',
            'x': '$position',
            'y': '$function',
            'line': {
                'color': 'purple'
            },
        },
        'Electron Density': {
            'name': 'Electron Density',
            'x': '$position',
            'y': '$function',
            'line': {
                'color': 'green'
            },
        },
        'Charge Density': {
            'name': 'Charge Density',
            'x': '$position',
            'y': '$function',
            'line': {
                'color': 'gray',
                'dash':'dash'
            },
            'unique' : True
        }
    },
    'layout': {
        'title': 'Doping, Electron and Hole Density',
        'showlegend': False,
        'yaxis': {
            'type': 'log',
            'title': 'Current Density (\cm3)',
            'exponentformat': 'e'
        },
        'xaxis': {
            'title': 'Position(um)'
        }
    },
    'normalize': True,
    'start_trace': 0,
}


POTENTIAL = {
    'id': 'net',
    'title': 'Electric Potential',
    'function': 'loadSequencePlotly',
    'dataset': {
        'Electrostatic Potential': {
            'name': 'Electrostatic Potential',
            'x': '$position',
            'y': '$delta',
            'line': {
                'color': '#1f77b4'
            },
        }
    },
    'layout': {
        'title': 'Net Charge Density',
        'showlegend': False,
        'yaxis': {
            'title': 'Potential (V)',
            'exponentformat': 'e'
        },
        'xaxis': {
            'title': 'Position(um)'
        }
    },
    'normalize': True,
    'start_trace': 0,
}


FIELD = {
    'id': 'field',
    'title': 'Electric Field',
    'function': 'loadSequencePlotly',
    'dataset': {
        'Electric Field': {
            'name': 'Electric Field',
            'x': '$position',
            'y': '$function',
            'line': {
                'color': '#1f77b4'
            },
        }
    },
    'layout': {
        'title':'Electrostatic Field',
        'showlegend': False,
        'yaxis': {
            'title' : 'Electric Fiueld (V/cm)',
            'exponentformat': 'e'
        },
        'xaxis': {
            'title': 'Position(um)'
        }
    },
    'normalize': True,
    'start_trace': 0
}


RECOMBINATION = {
    'id': 'recombination',
    'title': 'Recombination',
    'function': 'loadSequencePlotly',
    'dataset': {
        'Recombination Rate': {
            'name': 'Recombination Rate',
            'x': '$position',
            'y': '$function',
            'line': {
                'color': '#1f77b4'
            },
        }
    },
    'layout': {
        'title': 'Electrostatic Field',
        'showlegend': False,
        'yaxis': {
            'title': 'Recombination Rate (/cm^3s)',
            'exponentformat': 'e'
        },
        'xaxis': {
            'title': 'Position(um)'
        }
    },
    'normalize': True,
    'start_trace': 0
}


CARRIER = {
    'id': 'carrier',
    'title': 'Carrier Density',
    'function': 'loadSequencePlotly',
    'dataset': {
        'Excess Electron Density': {
            'name': 'Excess Electron Density',
            'x': '$position',
            'y': '$function',
            'line': {
                'color': 'purple'
            },
        }, 'Excess Hole Density': {
            'name': 'Excess Hole Density',
            'x': '$position',
            'y': '$function',
            'line': {
                'color': 'green'
            },
        }
    },
    'layout': {
        'title': 'Electrostatic Field',
        'showlegend': False,
        'yaxis': {
            'type': 'log',
            'title': 'Carrier Density (/cm^3)',
            'exponentformat': 'e'
        },
        'xaxis': {
            'title': 'Position(um)'
        }
    },
    'normalize': True,
    'start_trace': 1
}


DETAILS = {
    'id': 'squid',
    'title': 'More Details ...',
    'function': 'squidDetail',
}

PARAMS = {
    'id': 'parameters',
    'title': 'Input Params',
    'function' : 'loadHTML',
    'dataset' : {
        "Parameters": {
          'type':'div',
            'style':'padding:10px',
            'children':[{
                'type':'h2',
                'textContent':'Input Parameters'
            },
            {
                'type':'pre',
                'style':'overflow: auto;min-height: 50px',
                'textContent':'$value'
            }]
        }
    },
    'layout' : {},
}


s.outputs=[BANDS, IV, CV, TOTALCURRENT,DENSITY,ChargeDensity,POTENTIAL, FIELD, RECOMBINATION, CARRIER, PARAMS, DETAILS]


import base64
def encode_image(image_url):
    ext = image_url.split('.')[-1]
    prefix = f'data:image/{ext};base64,'
    with open(image_url, 'rb') as f:
        img = f.read()
    return prefix + base64.b64encode(img).decode('utf-8')


AppBar = t.TeleportElement(MaterialContent(elementType="AppBar"))
AppBar.content.attrs["position"] = "static"
AppBar.content.attrs["color"] = "primary"
AppBar.content.style = {"width": "inherit"}

ToolBar = t.TeleportElement(MaterialContent(elementType="Toolbar"))
ToolBar.content.attrs["variant"] = "regular"

Typography = t.TeleportElement(MaterialContent(elementType="Typography"))
Typography.content.attrs["variant"] = "h6"
Typography.content.style = {"flex": 1, "textAlign": "center"}
TypographyText = t.TeleportStatic(content="PN-Junction Lab")
Typography.addContent(TypographyText)

logo2 = t.TeleportElement(t.TeleportContent(elementType="img"))
logo2.content.attrs["width"] = "180"
logo2.content.attrs["src"] = encode_image("image.png")

logo = t.TeleportElement(t.TeleportContent(elementType="img"))
logo.content.attrs["width"] = "120"
logo.content.attrs["src"] = "https://nanohub.org/app/site/media/images/PressKit/nanoHUB_logo_color.jpg"

ToolBar.addContent(logo2)
ToolBar.addContent(Typography)
ToolBar.addContent(logo)
AppBar.addContent(ToolBar)

s.appbar = AppBar


from nanohubuidl.teleport import NanohubUtils
import re
import json

def refreshViews(tp, tc, *args, **kwargs):  
    eol = "\n"
    cache_store = kwargs.get("cache_store", "CacheStore");
    enable_compare = kwargs.get("enable_compare", True);
    views = kwargs.get("views", {});
    cache_storage = kwargs.get("cache_storage", "cacheFactory('"+cache_store+"', 'INDEXEDDB')")
    NanohubUtils.storageFactory(tp, store_name=cache_store, storage_name=cache_storage)          
    regc = tp.project_name    
    regc = "_" + re.sub("[^a-zA-Z0-9]+", "", regc) + "_"
    js = "async (component)=>{" + eol    
    js += "  let selfr = component;" + eol
    js += "  let listCache = [];" + eol
    js += "  let paramsCache = component.state.params" + eol
    js += "  if (!paramsCache || Object.keys(paramsCache).length === 0 && paramsCache.constructor === Object){" + eol
    js += "      paramsCache = await " + cache_store + ".getItem('cache_params');" + eol
    js += "      if (!paramsCache || paramsCache == '')" + eol
    js += "         paramsCache = {};" + eol
    js += "      else" + eol
    js += "         paramsCache = JSON.parse(paramsCache);" + eol
    js += "  }" + eol
    js += "  var activeCache = [];" + eol
    js += "  let enable_history = false;" + eol
    js += "  if (" + cache_store + "){" + eol
    if enable_compare:
        js += "    var olen = await " + cache_store + ".length();" + eol
        js += "    for (let ii=0; ii<olen; ii++) {" + eol
        js += "      var key = await " + cache_store + ".key(ii);" + eol
        js += "      //const regex = new RegExp('" + regc + "([a-z0-9]{64})', 'im');" + eol
        js += "      //let m;" + eol
        js += "      if (key.startsWith('" + regc + "')) {" + eol
        js += "        let m = [0,key.replace('" + regc + "','')];" + eol
        js += "        if (m[1].length == 64) {" + eol
        js += "          listCache.push(m[1]);" + eol
        js += "          if(!paramsCache[m[1]])" + eol
        js += "             paramsCache[m[1]] = m[1];" + eol
        js += "          if (component.state.lastCache == m[1]){ " + eol
        js += "            activeCache.push(m[1]);" + eol
        js += "          } else if (component.state.compare){ " + eol
        js += "            activeCache.push(m[1]);" + eol
        js += "            enable_history = true;" + eol
        js += "          } else {" + eol
        js += "            enable_history = true;" + eol
        js += "          }" + eol
        js += "        }" + eol
        js += "      }" + eol
        js += "    }" + eol
    else :
        js += "    if (component.state.lastCache != ''){" + eol
        js += "      activeCache.push(component.state.lastCache);" + eol
        js += "    }" + eol

    js += "    selfr.setState({'enable_history': enable_history, 'active_cache':activeCache, 'list_cache':listCache, 'params':paramsCache});" + eol
    js += "    let vis = selfr.state['visualization']; " + eol
    js += "    selfr.setState({'open_plot':selfr.state.visualization.id});" + eol
    for k,v in views.items():
        props = ["selfr"]
        state = {}
        name = str(k)
        if "params" in v:
            props = props + ["vis['" + str(v2) + "']" for v2 in v["params"]]
        if "state" in v:
            state = json.dumps(v["state"])
        js += "    if (vis['function'] == '"+name+"'){" + eol
        js += "        selfr.setState("+state+", () => {" + eol
        js += "          selfr.props."+name+"(" + ",".join(props) + ");" + eol
        js += "        });" + eol
        js += "    }" + eol
    js += "  }" + eol
    js += "}" + eol
    tc.addPropVariable("refreshViews", {"type":"func", 'defaultValue' :js})   

    return [
      {
        "type": "propCall2",
        "calls": "refreshViews",
        "args": ['self', '']
      }
    ] 

def deleteCurrent(tp, tc, *args, **kwargs):
    eol = "\n";
    cache_store = kwargs.get("cache_store", "CacheStore");
    cache_storage = kwargs.get("cache_storage", "cacheFactory('"+cache_store+"', 'INDEXEDDB')")
    NanohubUtils.storageFactory(tp, store_name=cache_store, storage_name=cache_storage)          

    regc = tp.project_name    
    regc = "_" + re.sub("[^a-zA-Z0-9]+", "", regc) + "_"

    js = "async (component)=>{" + eol    
    js += "  let selfr = component;" + eol
    js += "  var listState = [];" + eol
    js += "  var activeCache = [];" + eol
    js += "  let newstate = '';" + eol
    js += "  var olen = await " + cache_store + ".length();" + eol
    js += "  for (let ii=0; ii<olen; ii++) {" + eol
    js += "    var key = await " + cache_store + ".key(ii);" + eol
    js += "    const regex = new RegExp('" + regc + "([a-z0-9]{64})', 'im');" + eol
    js += "    let m;" + eol
    js += "    if ((m = regex.exec(key)) !== null) {" + eol
    js += "        if (component.state.lastCache == m[1]){ " + eol
    js += "            var deleted = await " + cache_store + ".removeItem(m[1]);" + eol
    js += "        } else { " + eol
    js += "            newstate = m[1] " + eol
    js += "        } " + eol
    js += "    };" + eol
    js += "  }" 
    js += "  selfr.setState({'lastCache':newstate});" + eol
    js += "  selfr.props.refreshViews(selfr);" + eol
    js += "}" + eol
    
    tc.addPropVariable("deleteCurrent", {"type":"func", 'defaultValue' :js})   

    return [
      {
        "type": "propCall2",
        "calls": "deleteCurrent",
        "args": ['self', '']
      }
    ] 

def buildThemeProvider(self, *args, **kwargs):
    eol = "\n";
    cache_store = kwargs.get("cache_store", "CacheStore");
    cache_storage = kwargs.get("cache_storage", "cacheFactory('"+cache_store+"', 'INDEXEDDB')")
    NanohubUtils.storageFactory(self.Project, store_name=cache_store, storage_name=cache_storage)          

    self.onDeleteCurrent = deleteCurrent(self.Project, self.Component)
    self.onRefreshViews = refreshViews(self.Project, 
                                       self.Component, 
                                       views=self.views,
                                       enable_compare=self.enable_compare) 
    self.Component.addStateVariable("list_cache", {"type":"array", "defaultValue": []})
    self.Component.addStateVariable("params", {"type":"object", "defaultValue": {}})
    js =  "(s, l, n)=>{" + eol    
    js += "  if (s.state.params && s.state.params[l] && s.state.params[l][n]){" + eol
    js += "    return s.state.params[l][n];" + eol
    js += "  } else {" + eol
    js += "    if (n == 'title'){" + eol
    js += "      return l;" + eol
    js += "    } else if (n == 'icon') { " + eol
    js += "      return (l==s.state.lastCache)?'primary':'primary';" + eol
    js += "    } else {" + eol
    js += "      return '';" + eol
    js += "    }" + eol
    js += "  }" + eol
    js += "}" + eol
    self.Component.addPropVariable("getParam", {"type":"func", "defaultValue": js})
    
    js =  "(s, e, n)=>{" + eol    
    js += "  if(s.state.lastCache && s.state.params){" + eol
    js += "    let paramsCache = {...s.state.params};" + eol
    js += "    if (!paramsCache[s.state.lastCache] || typeof paramsCache[s.state.lastCache] !== 'object')" + eol
    js += "      paramsCache[s.state.lastCache] = {}" + eol
    js += "    paramsCache[s.state.lastCache][n]= e;" + eol
    js += "    s.setState({'params': paramsCache});" + eol
    js += "    " + cache_store + ".setItem('cache_params', JSON.stringify(paramsCache));" + eol
    js += "  }" + eol
    js += "}" + eol
    self.Component.addPropVariable("setParam", {"type":"func", "defaultValue": js})
    
    
    SliderBar = t.TeleportElement(MaterialContent(elementType="Drawer"))
    SliderBar.content.attrs["variant"] = "persistent"
    SliderBar.content.attrs["open"] = True
    SliderBar.content.attrs["anchor"] = "right"
    SliderBar.content.style['width'] = "50px"
    SliderBar.content.style['backgroundColor'] = "#DBEAF0"
    SliderBar.content.style['overflow'] = "auto"
    SliderBar.content.style['margin'] = "0px"


    ToggleButton = t.TeleportElement(MaterialContent(elementType="ToggleButton"))
    ToggleButton.content.style['width'] = "50px"

    ToggleButton.content.attrs["value"] = "$index"

    Tooltip = t.TeleportElement(MaterialContent(elementType="Tooltip"))
    Tooltip.content.attrs["title"] = "$self.props.getParam(self, local, 'title')"
    Tooltip.content.attrs["placement"] = "left"
    placement="top"
    #<Badge badgeContent={4} color="primary">

    Badge = t.TeleportElement(MaterialContent(elementType="Badge"))
    Badge.content.attrs["badgeContent"] = " "
    Badge.content.attrs["variant"] = "dot"
    #Badge.content.attrs["color"] = "primary"
    Badge.content.attrs["color"] = "$self.props.getParam(self, local, 'icon')"

    Icon = t.TeleportElement(MaterialContent(elementType="Icon"))
    Icon.content.attrs["color"] = "$local == self.state.lastCache?self.props.getParam(self, local, 'icon'):'disabled'"
    #"id": "local == self.state.lastCache?'radio_button_checked':'radio_button_unchecked'"

    Icon.addContent(t.TeleportDynamic(content={
        "referenceType": "local",
        #"id": "local == self.state.lastCache?'radio_button_checked':'radio_button_unchecked'"
        "id": "local == self.state.lastCache?'bookmark':'bookmark_border'"
    }))  
    
    Badge.addContent(Icon) 
    Tooltip.addContent(Badge) 
    ToggleButton.addContent(Tooltip)  
    ToggleButton.content.events['click'] = [
        { "type": "stateChange", "modifies": "lastCache" ,"newState": "$local", "callbacks" : self.onRefreshViews}
    ]

    RepeatButton = t.TeleportRepeat(ToggleButton)
    RepeatButton.iteratorName = "local"
    RepeatButton.useIndex = True
    RepeatButton.dataSource = {
        "type": "dynamic",
        "content": {
            "referenceType": "state",
            "id": "list_cache"
        }
    }

    SliderBar.addContent(RepeatButton)
    
    ToggleButton2 = t.TeleportElement(MaterialContent(elementType="ToggleButton"))
    ToggleButton2.content.style['width'] = "50px"

    Tooltip2 = t.TeleportElement(MaterialContent(elementType="Tooltip"))
    Tooltip2.content.attrs["title"] = "Clear Current Run"
    Tooltip2.content.attrs["placement"] = "left"

    Icon2 = t.TeleportElement(MaterialContent(elementType="Icon"))
    Icon2.content.attrs["color"] = "$self.props.getParam(self, self.state.lastCache, 'icon')"

    icontext2 = t.TeleportStatic(content="delete")
    Icon2.addContent(icontext2)  
    Tooltip2.addContent(Icon2)  
    ToggleButton2.addContent(Tooltip2)  
    ToggleButton2.content.events['click'] = self.onDeleteCurrent

    
    ToggleButton3 = t.TeleportElement(MaterialContent(elementType="ToggleButton"))
    ToggleButton3.content.style['width'] = "50px"

    Tooltip3 = t.TeleportElement(MaterialContent(elementType="Tooltip"))
    Tooltip3.content.attrs["title"] = "Clear History"
    Tooltip3.content.attrs["placement"] = "left"

    Icon3 = t.TeleportElement(MaterialContent(elementType="Icon"))
    Icon3.content.attrs["color"] = "error"

    icontext3 = t.TeleportStatic(content="auto_delete")
    Icon3.addContent(icontext3)  
    Tooltip3.addContent(Icon3)  
    ToggleButton3.addContent(Tooltip3)  
    ToggleButton3.content.events['click'] = self.onDeleteHistory
    
    
    ToggleButton4 = t.TeleportElement(MaterialContent(elementType="ToggleButton"))
    ToggleButton4.content.style['width'] = "50px"

    Tooltip4 = t.TeleportElement(MaterialContent(elementType="Tooltip"))
    Tooltip4.content.attrs["title"] = "Configuration"
    Tooltip4.content.attrs["placement"] = "left"

    Icon4 = t.TeleportElement(MaterialContent(elementType="Icon"))
    Icon4.content.attrs["color"] = "$self.props.getParam(self, self.state.lastCache, 'icon')"

    icontext4 = t.TeleportStatic(content="settings")
    Icon4.addContent(icontext4)
    Tooltip4.addContent(Icon4)
    ToggleButton4.addContent(Tooltip4)
    ToggleButton4.content.events['click'] = [{ "type": "stateChange", "modifies": "dialog_open","newState": True}]
    
    SliderBar.addContent(ToggleButton4)
    SliderBar.addContent(ToggleButton2)
    SliderBar.addContent(ToggleButton3)

    a = UIDLConstructor.buildThemeProvider(self)
    a.content.children[3].content.children[1].addContent(SliderBar)
            
        
    self.Component.addStateVariable("dialog_open", {"type":"bool", "defaultValue":False})

    PDialog = t.TeleportElement(MaterialContent(elementType="Dialog"))
    PDialog.content.attrs['open'] = {
        "type": "dynamic",
        "content": {
            "referenceType": "state",
            "id": "dialog_open"
        }
    }
    PDialogTitle = t.TeleportElement(MaterialContent(elementType="DialogTitle"))

    PDialogContent = t.TeleportElement(MaterialContent(elementType="DialogContent"))
    PDialogText = t.TeleportElement(MaterialContent(elementType="DialogContentText"))
    PTextField = t.TeleportElement(MaterialContent(elementType="TextField"))
    PTextField.content.attrs['autoFocus'] = True
    PTextField.content.attrs['margin'] = "dense"
    PTextField.content.attrs['label'] = "Description"
    PTextField.content.attrs['type'] = "text"
    PTextField.content.attrs['fullWidth'] = True
    PTextField.content.attrs['variant'] = "standard"
    PTextField.content.attrs['defaultValue'] = "$self.props.getParam(self, self.state.lastCache, 'title')"
    PTextField.content.events['onBlur'] = [{
        "type": "propCall2",
        "calls": "setParam",
        "args": ['self', 'e.target.value', "'title'"]
    }]
    
    PRadioGroup = t.TeleportElement(MaterialContent(elementType="RadioGroup"))
    PRadioGroup.content.attrs['row'] = True
    colors = ['action','primary','secondary','error','info','success','warning']
    for c in colors:
        PRadio = t.TeleportElement(MaterialContent(elementType="Icon"))
        PRadio.content.attrs['color'] = c
        PRadio.addContent(t.TeleportStatic(content="bookmark"))
        CPRadio = t.TeleportConditional(t.TeleportStatic(content="_border"))
        CPRadio.reference = {
            "type": "dynamic",
            "content": {
                "referenceType": "prop",
                "id": "getParam(self, self.state.lastCache, 'icon') == '" + c + "'"
            }
        }    
        CPRadio.value = False
        CPRadio.conditions =[{"operation" : "=="}]
        PRadio.addContent(CPRadio)
        PRadio.content.events['onClick'] = [{
            "type": "propCall2",
            "calls": "setParam",
            "args": ['self', "'" + c + "'", "'icon'"]
        }]
        PRadioGroup.addContent(PRadio)

    
    PDialogActions = t.TeleportElement(MaterialContent(elementType="DialogActions"))
    PButton = t.TeleportElement(MaterialContent(elementType="Button"))
    PCButton = t.TeleportStatic(content="Close")
    PButton.addContent(PCButton)

    PButton.content.events['click'] = [{ "type": "stateChange", "modifies": "dialog_open","newState": False}]

    PDialog.addContent(PDialogTitle)
    PDialog.addContent(PDialogContent)
    PDialog.addContent(PDialogActions)
    
    PDialogTitle.addContent(t.TeleportStatic(content="Simulation Properties"))

    PDialogContent.addContent(PDialogText)
    PDialogText.addContent(t.TeleportStatic(content="Please describe the simulation identified with squid ("))
    PDialogText.addContent(t.TeleportDynamic(content={"referenceType": "state","id": "lastCache"}))
    PDialogText.addContent(t.TeleportStatic(content=")"))

    PDialogContent.addContent(PTextField)
    PDialogContent.addContent(PRadioGroup)

    PDialogActions.addContent(PButton)

    a.content.children[3].content.children[1].addContent(PDialog)
    
    return a
from types import MethodType
s.buildThemeProvider = MethodType(buildThemeProvider, s)




try:
    w = s.assemble(
        jupyter_notebook_url=jupyter_notebook_url, 
        uidl_local = True,
        copy_libraries=False,
        widget = False,    
    )
    display(w)
except:
    s.OUTFILE = "PNJUNCTIONAPP.HTML"
    s.assemble(jupyter_notebook_url="", copy_libraries=True)







