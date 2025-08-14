import Typography from '@mui/material/Typography';

const EditableField = ({ label, value, isEditing, onChange, type = 'input', multiline = false, name }) => {
    return (
        <Typography variant="body1" gutterBottom>
            <strong>{label}:</strong> {isEditing ? (
                multiline ? (
                    <textarea
                        name={name || label.toLowerCase().replace(' ', '_')}
                        value={value || ''}
                        onChange={onChange}
                    />
                ) : (
                    <input
                        type={type}
                        name={name || label.toLowerCase().replace(' ', '_')}
                        value={value || ''}
                        onChange={onChange}
                        {...(type === 'number' && {
                            onInput: (e) => {
                                console.log(e.target.valueAsNumber)
                                if (e.target.valueAsNumber < 0) {
                                    e.target.valueAsNumber = 0
                                }
                            },
                            onKeyDown: (e) => {
                                if (!(/[0-9]/.test(e.key) || e.key === 'Backspace')) {
                                    e.preventDefault();
                                }
                            }
                        })}
                    />
                )
            ) : (
                value || 'None'
            )}
        </Typography>
    );
};

export default EditableField;