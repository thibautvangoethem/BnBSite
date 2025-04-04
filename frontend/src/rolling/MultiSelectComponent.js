import React, { useState } from 'react';
import {
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    Checkbox,
    ListItemText,
    Box,
} from '@mui/material';

const MultiSelectComponent = ({ selectionData }) => {
    const [selectedItems, setSelectedItems] = useState(
        selectionData.map(() => [])
    );

    const handleChange = (event, index) => {
        const value = event.target.value;
        const newSelectedItems = [...selectedItems];
        newSelectedItems[index] =
            typeof value === 'string' ? value.split(',') : value;
        setSelectedItems(newSelectedItems);
    };

    return (
        <Box>
            {selectionData.map((selection, index) => (
                <Box key={index} sx={{ minWidth: 200, marginBottom: 2 }}>
                    <FormControl fullWidth>
                        <InputLabel>{selection.label}</InputLabel>
                        <Select
                            label={selection.label}
                            multiple
                            value={selectedItems[index]}
                            onChange={(event) => handleChange(event, index)}
                            renderValue={(selected) => selected.join(', ')}
                        >
                            {selection.options.map((item, itemIndex) => (
                                <MenuItem key={itemIndex} value={item}>
                                    <Checkbox
                                        checked={selectedItems[index].indexOf(item) > -1}
                                    />
                                    <ListItemText primary={item} />
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </Box>
            ))}
        </Box>
    );
};

export default MultiSelectComponent;
