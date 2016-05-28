\copy (Select * From ceeb_program_internationalenglishtest ) To '/tmp/ceeb_program_internationalenglishtest.csv' With CSV HEADER;
\copy (Select * From ceeb_program_cost ) To '/root/newdump/ceeb_program_cost.csv' With CSV HEADER;
\copy (Select * From ceeb_program_curriculumunit ) To '/root/newdump/ceeb_program_curriculumunit.csv' With CSV HEADER;
\copy (Select * From ceeb_program_program_subject ) To '/root/newdump/ceeb_program_program_subject.csv' With CSV HEADER;
\copy (Select * From ceeb_program_deadline ) To '/root/newdump/ceeb_program_deadline.csv' With CSV HEADER;
\copy (Select * From ceeb_program_durationunit ) To '/root/newdump/ceeb_program_durationunit.csv' With CSV HEADER;
\copy (Select * From ceeb_program_eventtype ) To '/root/newdump/ceeb_program_eventtype.csv' With CSV HEADER;
\copy (Select * From ceeb_program_degreeref ) To '/root/newdump/ceeb_program_degreeref.csv' With CSV HEADER;
\copy (Select * From ceeb_program_program ) To '/root/newdump/ceeb_program_program.csv' With CSV HEADER;
\copy (Select * From ceeb_program_exam ) To '/root/newdump/ceeb_program_exam.csv' With CSV HEADER;
\copy (Select * From ceeb_program_requirement ) To '/root/newdump/ceeb_program_requirement.csv' With CSV HEADER;
\copy (Select * From ceeb_program_internalcode ) To '/root/newdump/ceeb_program_internalcode.csv' With CSV HEADER;
\copy (Select * From ceeb_program_requirement_intl_transcript ) To '/root/newdump/ceeb_program_requirement_intl_transcript.csv' With CSV HEADER;
\copy (Select * From ceeb_program_expertnotes ) To '/root/newdump/ceeb_program_expertnotes.csv' With CSV HEADER;
\copy (Select * From ceeb_program_tuitionunit ) To '/root/newdump/ceeb_program_tuitionunit.csv' With CSV HEADER;
\copy (Select * From ceeb_program_subject ) To '/root/newdump/ceeb_program_subject.csv' With CSV HEADER;
\copy (Select * From ceeb_program_universityschool ) To '/root/newdump/ceeb_program_universityschool.csv' With CSV HEADER;
\copy (Select * From ceeb_program_transcriptevaluationprovider ) To '/root/newdump/ceeb_program_transcriptevaluationprovider.csv' With CSV HEADER;
\copy (Select * From ceeb_program_scholarship ) To '/root/newdump/ceeb_program_scholarship.csv' With CSV HEADER;
