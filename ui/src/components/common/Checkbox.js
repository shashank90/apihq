export default function Checkbox(props) {
  const name = props.name;
  const label = props.label;
  const checked = props.checked;
  const onChange = props.onChange;

  return (
    <div>
      <input
        type="checkbox"
        name={name}
        checked={checked}
        onChange={onChange}
      />
      <label>{label}</label>
    </div>
  );
}
