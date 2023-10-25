import * as React from 'react';
import {
    List,
    Datagrid,
    TextField,
    NumberField,
    DateInput,
    EmailField,
    DateField,
    FunctionField,
} from 'react-admin';

const listFilters = [
    <DateInput source="start_date" alwaysOn />,
    <DateInput source="end_date" alwaysOn />,
];

export const LeadList = () => (
    <List
        filters={listFilters}
        perPage={25}
        sort={{field: 'id', order: 'desc'}}
    >
        <Datagrid
            rowClick="show"
            sx={{
                '& .column-customer_id': {
                    display: {xs: 'none', md: 'table-cell'},
                },
                '& .column-total_ex_taxes': {
                    display: {xs: 'none', md: 'table-cell'},
                },
                '& .column-delivery_fees': {
                    display: {xs: 'none', md: 'table-cell'},
                },
                '& .column-taxes': {
                    display: {xs: 'none', md: 'table-cell'},
                },
            }}
        >
            <NumberField source="id" />
            <TextField source="first_name" />
            <TextField source="last_name" />
            <TextField source="provider_name" />
            <EmailField source="email" />
            <DateField source="created_date"/>

            <FunctionField label="Courses" render={(record) => record.courses.length} />
        </Datagrid>
    </List>
);

export default LeadList;
