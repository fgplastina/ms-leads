import {
    SelectArrayInput,
    Edit,
    NumberInput,
    SimpleForm,
    ReferenceInput,
    SelectInput,
    TextInput,
    FormDataConsumer,
    DateInput,
    required,
} from 'react-admin';


export const LeadEdit = () => (
    <Edit>
        <SimpleForm>
            <TextInput source="first_name" validate={required()} />
            <TextInput source="last_name" validate={required()} />
            <TextInput source="email" validate={required()} />
            <TextInput source="address" validate={required()} />
            <TextInput source="phone" validate={required()} />
            <DateInput source="inscription_year" validate={required()} />
            <NumberInput source="number_of_times_taken" validate={required()} />

            <ReferenceInput label="Career:" source="career_id" reference="careers" validate={required()}>
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
    </Edit>
);

export default LeadEdit;
