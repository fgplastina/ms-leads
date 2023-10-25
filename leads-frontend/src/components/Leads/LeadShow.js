import {
    SimpleShowLayout,
    Show,
    TextField,
    DateField,
    NumberField,
    ReferenceField,
    SingleFieldList,
    ChipField,
    ReferenceArrayField
} from 'react-admin';

const LeadShow = (props) => (
    <Show {...props}>
        <SimpleShowLayout>
            <TextField source="first_name" label="First Name" />
            <TextField source="last_name" label="Last Name" />
            <TextField source="email" label="Email" />
            <TextField source="address" label="Address" />
            <TextField source="phone" label="Phone" />
            <DateField source="inscription_year" label="Inscription Year" />
            <NumberField source="number_of_times_taken" label="Number of Times Taken" />
            <ReferenceField label="Career" source="career_id" reference="careers">
                <TextField source="name" />
            </ReferenceField>
            <ReferenceArrayField label="Courses" reference="courses" source="courses" linkType={false}>
                <SingleFieldList link={false}>
                    <ChipField source="name" />
                </SingleFieldList>
            </ReferenceArrayField>
        </SimpleShowLayout>
    </Show>
);

export default LeadShow;
