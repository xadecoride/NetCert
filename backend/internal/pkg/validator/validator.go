// Package validator provides a shared validator instance for use across
// delivery handlers. The underlying library is go-playground/validator/v10.
package validator

import (
	"fmt"

	"github.com/go-playground/validator/v10"
	"github.com/netcert/backend/internal/domain"
)

// v is the singleton validator. Using a singleton is safe because the
// underlying validator is stateless (per the library docs) after
// construction with a single registered set of struct-level tags.
var v *validator.Validate

func init() {
	v = validator.New()
}

// Struct validates a struct's fields using the `validate` struct tags and
// returns a human-readable error string on failure. Returns nil when
// validation passes.
//
// Example usage in a handler:
//
//	if err := validator.Struct(req); err != nil {
//	    writeJSON(w, http.StatusBadRequest, map[string]string{"error": err.Error()})
//	    return
//	}
func Struct(s interface{}) error {
	if err := v.Struct(s); err != nil {
		// Convert field errors into a single readable message.
		if ve, ok := err.(validator.ValidationErrors); ok {
			msg := formatValidationErrors(ve)
			return fmt.Errorf("%w: %s", domain.ErrValidation, msg)
		}
		return err
	}
	return nil
}

func formatValidationErrors(ves validator.ValidationErrors) string {
	if len(ves) == 0 {
		return "validation failed"
	}
	// Show only the first error for simplicity; users can resubmit.
	fe := ves[0]
	switch fe.Tag() {
	case "required":
		return fmt.Sprintf("field %s is required", fe.Field())
	case "email":
		return fmt.Sprintf("field %s must be a valid email", fe.Field())
	case "min":
		return fmt.Sprintf("field %s must be at least %s characters", fe.Field(), fe.Param())
	case "max":
		return fmt.Sprintf("field %s must be at most %s characters", fe.Field(), fe.Param())
	case "oneof":
		return fmt.Sprintf("field %s must be one of: %s", fe.Field(), fe.Param())
	default:
		return fmt.Sprintf("field %s failed %s validation", fe.Field(), fe.Tag())
	}
}
