import * as React from 'react';
import Box from '@mui/material/Box';
import FormLabel from '@mui/material/FormLabel';
import FormControl from '@mui/material/FormControl';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormHelperText from '@mui/material/FormHelperText';
import Checkbox from '@mui/material/Checkbox';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Paper from '@mui/material/Paper';
import Icon from '@mui/material/Icon';

function DiagnosticPage() {

	/* SINTOMAS */
	const [state, setState] = React.useState({
		tos: false,
		fiebre: false,
		mocos: false,
		dificultadRespiratoria: false,
		dolorMuscular: false,
		decaimiento: false,
		diarrea: false,
		vomitos: false,
	});

	const handleSymptomsChange = (event) => {
		setState({
			...state,
			[event.target.name]: event.target.checked,
		});
	};

	const {
		tos,
		fiebre,
		mocos,
		dificultadRespiratoria,
		dolorMuscular,
		decaimiento,
		diarrea,
		vomitos,
	} = state;

	/* ESTADO PACIENTE */

	const [clinicState, setClinicState] = React.useState('ESTABLE');

	const handleClinicStateChange = (event) => {
		setClinicState((event.target).value);
	};

	/* RESULTADO COVID */

	const [covidTestResultState, setCovidTestResultState] = React.useState('NEGATIVO');

	const handleCovidTestResultChange = (event) => {
		setCovidTestResultState((event.target).value);
	};


	/* RESULTADOS */

	const [results, setResults] = React.useState(null);

	const getResults = async () => {
		const returnedResults = await fetch('http://localhost:5000/analisis', {
			method: 'POST',
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				hisopado: covidTestResultState,
				sintomasPaciente: Object.values(state).filter((x)=>x).length,
				estadoClinico: clinicState,
			})
  	});
		setResults(await returnedResults.json());
	};

	if (!results) {
		return (
			<Box sx={{ display: 'flex', justifyContent: 'center' }}>
				<FormControl sx={{ m: 3 }} component="fieldset" variant="standard">
					<Paper elevation={3} sx={{mt: 2, p: 2, borderRadius: 4}}>
						<FormLabel component="legend">¿Que sintomas tiene el paciente?</FormLabel>
						<FormGroup>
							<FormControlLabel
								control={
									<Checkbox checked={tos} onChange={handleSymptomsChange} name="tos" />
								}
								label="Tos"
							/>
							<FormControlLabel
								control={
									<Checkbox checked={fiebre} onChange={handleSymptomsChange} name="fiebre" />
								}
								label="Fiebre"
							/>
							<FormControlLabel
								control={
									<Checkbox checked={mocos} onChange={handleSymptomsChange} name="mocos" />
								}
								label="Mocos"
							/>
							<FormControlLabel
								control={
									<Checkbox checked={dificultadRespiratoria} onChange={handleSymptomsChange} name="dificultadRespiratoria" />
								}
								label="Dificultad respiratoria"
							/>
							<FormControlLabel
								control={
									<Checkbox checked={dolorMuscular} onChange={handleSymptomsChange} name="dolorMuscular" />
								}
								label="Dolor muscular"
							/>
							<FormControlLabel
								control={
									<Checkbox checked={decaimiento} onChange={handleSymptomsChange} name="decaimiento" />
								}
								label="Decaimiento"
							/>
							<FormControlLabel
								control={
									<Checkbox checked={diarrea} onChange={handleSymptomsChange} name="diarrea" />
								}
								label="Diarrea"
							/>
							<FormControlLabel
								control={
									<Checkbox checked={vomitos} onChange={handleSymptomsChange} name="vomitos" />
								}
								label="Vómitos"
							/>
						</FormGroup>
					</Paper>

					<Paper elevation={3} sx={{mt:2, p: 2, borderRadius: 4}}>
						<FormLabel id="demo-radio-buttons-group-label">¿Cual es el estado clínico del paciente?</FormLabel>
						<RadioGroup
							aria-labelledby="demo-radio-buttons-group-label"
							name="radio-buttons-group"
							value={clinicState}
							onChange={handleClinicStateChange}
						>
							<FormControlLabel value="ESTABLE" control={<Radio />} label="Estable" />
							<FormControlLabel value="DE_GRAVEDAD" control={<Radio />} label="De gravedad" />
						</RadioGroup>
					</Paper>

					<Paper elevation={3} sx={{mt: 2, p: 2, borderRadius: 4}}>
						<FormLabel id="demo-radio-buttons-group-label">¿Cual fue el resultado del hisopado?</FormLabel>
						<RadioGroup
							aria-labelledby="demo-radio-buttons-group-label"
							name="radio-buttons-group"
							value={covidTestResultState}
							onChange={handleCovidTestResultChange}
						>
							<FormControlLabel value="NEGATIVO" control={<Radio />} label="Negativo" />
							<FormControlLabel value="POSITIVO" control={<Radio />} label="Positivo" />
							<FormControlLabel value="NO_DISPONIBLE" control={<Radio />} label="Aún no disponible" />

						</RadioGroup>
					</Paper>

					<Button sx={{mt: 2}} variant="contained" endIcon={<SendIcon />} onClick={()=>(getResults())}>
						Enviar
					</Button>
				</FormControl>
			</Box>
		);
	} else {
		return (
			<Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
				<Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
					<Paper elevation={3} sx={{mt: 2, p: 2, borderRadius: 4}}>
						<h2>¿Como continuar?</h2>
						<Box sx={{ width: '300px' }}>
								<h3>Paciente</h3>
								<List>
									{results.sugerencias_paciente.map((value, index) => (
										<ListItem key={index}>
											<Box sx={{
												backgroundColor: 'black',
												height: '6px',
												width: '6px',
												borderRadius: '5px',
												mr: 1,
											}} />
											<ListItemText
												primary={value}
											/>
										</ListItem>
									))}
								</List>
						</Box>

						<Box sx={{ width: '300px' }}>
									<h3>Contactos Estrechos</h3>
									<List>
										{results.sugerencias_contactos_estrechos.map((value, index) => (
											<ListItem key={index}>
												<Box sx={{
													backgroundColor: 'black',
													height: '6px',
													width: '6px',
													borderRadius: '5px',
													mr: 1,
												}} />
												<ListItemText
													primary={value}
												/>
											</ListItem>
										))}
									</List>
						</Box>
					</Paper>
				</Box>
				<Box sx={{
					display: 'flex',
					flexDirection: 'column',
					alignItems: 'center',
					rowGap: '15px',
					mt: 2,
				}}>
					<Button variant="contained" onClick={()=>(setResults(null))}>
						Realizar otro diagnostico
					</Button>

					<Button variant="contained">
						Exportar resultado
					</Button>
				</Box>
			</Box>
		);
	}
}

export default DiagnosticPage;