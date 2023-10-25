import React from 'react';
import {Admin, Resource, Layout, Title} from 'react-admin';

import simpleRestProvider from 'ra-data-simple-rest';
import {LeadList, LeadCreate, LeadEdit, LeadShow} from './components/Leads'


const apiUrl = 'http://localhost:8000';

const AppAdmin = () => {

  return (

    <Admin
      dataProvider={simpleRestProvider(apiUrl)}
      defaultTheme="light"
      layout={Layout}
      darkTheme={{palette: {mode: 'dark'}}}
    >
      <Title title="Leads" />
      <Resource name="leads" list={LeadList} edit={LeadEdit} show={LeadShow} create={LeadCreate} />
    </Admin>
  )
};

export default AppAdmin;

