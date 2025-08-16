import { useState, useEffect, useCallback } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { useNavigate } from "react-router";

const HistoryGrid = () => {
    const backendUrl = process.env.REACT_APP_BACKEND_URL;
    const apiTypeMap = {
        "Gun": "gun",
        "Potion": "potion",
        "Shield": "shield",
        "Grenade": "grenade",
        "Classmod": "classmod"
    }
    const [rows, setRows] = useState();
    const navigate = useNavigate();

    const handleRowClick = (params) => {
        console.log(params.row);
        navigate(`/viz/${apiTypeMap[params.row.type]}/${params.row.id}`);
    };


    useEffect(() => {

        // Hide the resizeobserver error in dev mode
        // It triggers when you increase the grid collumn width to go beyond the viewport. I dont know why this is a problem, every grid system I used before this handles this by simply decreasing last collumn size/blocking the action.
        // The grid will still grow a bit along increasing the page (yay scrolbar) but it wont error after this
        // 'closed' earlier this year https://github.com/adazzle/react-data-grid/issues/3314 (below hack also taken from there)
        // I am probably messing something basic up here, but the error/google/doc is not being helpfull in pointing me the correct way.
        // React/Javascript is my passion
        const resizeObserverErrHandler = (e) => {
            if (e.message === 'ResizeObserver loop completed with undelivered notifications.') {
                const resizeObserverErrDiv = document.getElementById('webpack-dev-server-client-overlay-div');
                const resizeObserverErr = document.getElementById('webpack-dev-server-client-overlay');
                if (resizeObserverErr) {
                    resizeObserverErr.setAttribute('style', 'display: none');
                }
                if (resizeObserverErrDiv) {
                    resizeObserverErrDiv.setAttribute('style', 'display: none');
                }

            }
        };

        window.addEventListener('error', resizeObserverErrHandler);

        fetchData();

        return () => {
            window.removeEventListener('error', resizeObserverErrHandler);
        };
    }, []);

    const fetchData = useCallback(async () => {
        try {
            const response = await fetch(`${backendUrl}/rollhistory/get_all`);
            const data = await response.json();
            setRows(data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }, [backendUrl]);




    const columns = [
        { field: 'id', headerName: 'ID', width: 200 },
        { field: 'date', headerName: 'Roll Date', width: 250 },
        { field: 'type', headerName: 'Type', width: 130 },
        { field: 'description', headerName: 'Description', flex: 1 },
    ];

    return (
        <div style={{ height: '100vh', width: '100%' }}>
            <DataGrid
                rows={rows}
                columns={columns}
                pageSize={5}
                onRowClick={handleRowClick}
                style={{ height: 'calc(100vh - 100px)', width: '100%', overflowY: 'scroll' }}
            />
        </div>
    );
};

export default HistoryGrid;