import {
    SelectArrayInput,
    Create,
    NumberInput,
    SimpleForm,
    ReferenceInput,
    SelectInput,
    TextInput,
    FormDataConsumer,
    DateInput
} from 'react-admin';


export const LeadCreate = () => (
    <Create>
        <SimpleForm>
            <TextInput source="first_name" />
            <TextInput source="last_name" />
            <TextInput source="email" />
            <TextInput source="address" />
            <TextInput source="phone" />
            <DateInput source="inscription_year" />
            <NumberInput source="number_of_times_taken" />

            <ReferenceInput label="Career:" source="career_id" reference="careers">
                <SelectInput optionText="name" />
            </ReferenceInput>

            <FormDataConsumer>
                {({formData, ...rest}) => (
                    formData.career_id ? (
                        <ReferenceInput
                            label="Courses"
                            source="courses"
                            reference="courses"
                            filter={{career_id: formData.career_id}}
                        >
                            <SelectArrayInput optionText="name" {...rest} />
                        </ReferenceInput>
                    ) : null
                )}
            </FormDataConsumer>



        </SimpleForm>
    </Create>
);

export default LeadCreate;
