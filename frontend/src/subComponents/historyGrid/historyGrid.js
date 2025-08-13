import { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { TextField, Button } from '@mui/material';

const HistoryGrid = () => {
    const [rows, setRows] = useState([
        { id: 1, rollDate: '2023-01-01', type: 'Type A', name: 'John Doe' },
        { id: 2, rollDate: '2023-01-02', type: 'Type B', name: 'Jane Smith' },
        { id: 3, rollDate: '2023-01-03', type: 'Type C', name: 'Bob Johnson' },

    ]);
    const [filters, setFilters] = useState({
        name: '',
        type: '',

    });

    const handleRowClick = (params) => {
        console.log(params.row);
    };



    const fetchData = async () => {
        try {
            // Replace 'YOUR_API_ENDPOINT' with your actual API endpoint
            // const response = await fetch(`YOUR_API_ENDPOINT?search=${filters.searchTerm}`);
            // const data = await response.json();
            const data = rows.filter(row =>
                row.name.toLowerCase().includes(filters.searchTerm.toLowerCase())
            );
            setRows(data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    useEffect(() => {
        fetchData();
    }, [filters]);

    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        setFilters((prevFilters) => ({
            ...prevFilters,
            [name]: value,
        }));
    };

    const handleFilterSubmit = (e) => {
        e.preventDefault();
        fetchData();
    };

    const columns = [
        { field: 'id', headerName: 'ID', width: 70 },
        { field: 'rollDate', headerName: 'Roll Date', width: 130 },
        { field: 'type', headerName: 'Type', width: 130 },
        { field: 'name', headerName: 'Name', width: 130 },
    ];

    return (
        <div style={{ height: '100vh', width: '100%' }}>
            <form onSubmit={handleFilterSubmit}>
                <TextField
                    label="Name"
                    name="name"
                    value={filters.name}
                    onChange={handleFilterChange}
                />
                <TextField
                    label="Type"
                    name="type"
                    value={filters.type}
                    onChange={handleFilterChange}
                />
                <Button type="submit" variant="contained" color="primary">
                    Apply Filters
                </Button>
            </form>
            <DataGrid
                rows={rows}
                columns={columns}
                pageSize={5}
                onRowClick={handleRowClick}
                style={{ height: 'calc(100vh - 100px)', width: '100%' }}

            />

        </div>
    );
};

export default HistoryGrid;